import express from 'express'

const app = express()
const port = 3000;



app.listen(port, () => {
    console.log(`Servidor rodando na porta ${port}`)
})

app.get("/", (req, res) => {
    res.send("<h1>Hello bitches</h1>")
})

app.get("/contact", (req, res) => {
    res.send("<h2>11 950861903</h2>")
})


app.get("/about", (req, res) => {
    res.send("<h1>About me</h1><p>I dont know</p>")
})
