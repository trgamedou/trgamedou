import weaviate from "weaviate-ts-client"
import fs from "fs"

const client = weaviate.client({ scheme: 'http', host: 'localhost:8080' })

/**
 * #region
 * Creating the Schema
 */

const schemaConfig = {
    class: 'ProductImages',
    vectorizer: "img2vec-neural",
    vectorIndexType: 'hnsw',
    moduleConfig: {
        'img2vec-neural': {
            imageFields: ['image']
        }
    },
    properties: [{ name: 'image', dataType: ['blob'] }, { name: 'text', dataType: ['string'] }]
}

await client.schema.classCreator().withClass(schemaConfig).do()
const schemaRes = await client.schema.getter().do()
console.log(schemaRes)

/**
 * #region
 * Batch Imports
 */

const batchImport = async () => {
    const images = fs.readdirSync('./images');

    // Prepare a batcher
    let batcher = client.batch.objectsBatcher();
    let counter = 0;
    let batchSize = 100;

    for (const image of images) {
        const b64 = Buffer.from(fs.readFileSync(`./images/${image}`)).toString("base64");

        // Construct an object with a class and properties 'image' and 'text'
        const obj = {
            class: "ProductImages",
            properties: {
                image: b64,
                text: image.split(".")[0].split('_').join(' ')
            }
        }

        // add the object to the batch queue
        batcher = batcher.withObject(obj)

        // When the batch counter reaches batchSize, push the objects to Weaviate
        if (counter++ == batchSize) {
            // flush the batch queue
            await batcher.do();
    
            // restart the batch queue
            counter = 0;
            batcher = client.batch.objectsBatcher();
        }
    }

    // Flush the remaining objects
    await batcher.do()
}

await batchImport();

/**
 * #region
 * Comparison
 */

const imgFiles = fs.readdirSync('./input-images');

const promises = imgFiles.map(
    async (imgFile) => {
        const image = Buffer.from(fs.readFileSync(`./input-images/${imgFile}`)).toString("base64");

        const resImage = await client.graphql
            .get()
            .withClassName('ProductImages')
            .withFields(['_additional { distance }', 'text'])
            .withNearImage({ image, distance: 0.05 })
            .do();

        const matches = resImage.data.Get.ProductImages.length;

        if (matches) {
            console.log({
                matches,
                image: imgFile.split(".")[0].split('_').join(' '),
                matchedImages: resImage.data.Get.ProductImages.map(({ text }) => text),
            })
        }

    }
)

await Promise.all(promises)
