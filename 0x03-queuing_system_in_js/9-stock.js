import express from 'express';
import redis from 'redis';
import { promisify } from 'util';

// Create an Express application
const app = express();
const PORT = 1245;

// Data: List of products
const listProducts = [
    { itemId: 1, itemName: 'Suitcase 250', price: 50, initialAvailableQuantity: 4 },
    { itemId: 2, itemName: 'Suitcase 450', price: 100, initialAvailableQuantity: 10 },
    { itemId: 3, itemName: 'Suitcase 650', price: 350, initialAvailableQuantity: 2 },
    { itemId: 4, itemName: 'Suitcase 1050', price: 550, initialAvailableQuantity: 5 }
];

// Redis client setup
const redisClient = redis.createClient();
const getAsync = promisify(redisClient.get).bind(redisClient);
const setAsync = promisify(redisClient.set).bind(redisClient);

// Function to reserve stock by itemId
const reserveStockById = async (itemId, stock) => {
    await setAsync(`item.${itemId}`, stock);
};

// Function to get current reserved stock by itemId
const getCurrentReservedStockById = async (itemId) => {
    const reservedStock = await getAsync(`item.${itemId}`);
    return reservedStock ? parseInt(reservedStock) : 0;
};

// Function to get item by ID
const getItemById = (id) => {
    return listProducts.find(item => item.itemId === id);
};

// Middleware to parse JSON bodies
app.use(express.json());

// Route to list all available products
app.get('/list_products', (req, res) => {
    res.json(listProducts.map(item => ({
        itemId: item.itemId,
        itemName: item.itemName,
        price: item.price,
        initialAvailableQuantity: item.initialAvailableQuantity
    })));
});

// Route to get product details by itemId
app.get('/list_products/:itemId', async (req, res) => {
    const { itemId } = req.params;
    const item = getItemById(parseInt(itemId));
    if (!item) {
        return res.json({ status: 'Product not found' });
    }
    const currentQuantity = item.initialAvailableQuantity - await getCurrentReservedStockById(itemId);
    res.json({ ...item, currentQuantity });
});

// Route to reserve a product by itemId
app.get('/reserve_product/:itemId', async (req, res) => {
    const { itemId } = req.params;
    const item = getItemById(parseInt(itemId));
    if (!item) {
        return res.json({ status: 'Product not found' });
    }
    const currentReservedStock = await getCurrentReservedStockById(itemId);
    if (currentReservedStock >= item.initialAvailableQuantity) {
        return res.json({ status: 'Not enough stock available', itemId: parseInt(itemId) });
    }
    await reserveStockById(itemId, currentReservedStock + 1);
    res.json({ status: 'Reservation confirmed', itemId: parseInt(itemId) });
});

// Start the Express server
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});

