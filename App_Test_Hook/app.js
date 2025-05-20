var express = require('express');
var app = express();
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

const port = 3000;

app.all('/*', function (req, res) {
   console.log("-------------- New Request --------------");
   const shopDomain = req.get('X-Shopify-Shop-Domain')
   //console.log("Headers:"+ JSON.stringify(req.headers, null, 3));
   console.log("Entrada:"+ JSON.stringify(req.body, null, 3));
   console.log("Dominio:", shopDomain);
   
   res.json({ message: "Thank you for the message" });
})

app.listen(port, function () {
   console.log(`Servidor iniciado en el puerto ${port}`)
})
