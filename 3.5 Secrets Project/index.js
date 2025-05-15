import express from "express";
import { dirname } from "path";
import { fileURLToPath } from "url";
const __dirname = dirname(fileURLToPath(import.meta.url));

const app = express();

app.get("/check", (req, res) => {
    res.sendFile(__dirname + "public/index.html")
})

