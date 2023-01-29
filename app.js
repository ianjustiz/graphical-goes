const http = require("http");
const fs = require("fs").promises;

const hostname = '127.0.0.1';
const port = 3000;

const server = http.createServer((req, res) => {
  res.statusCode = 200;
  res.setHeader('Content-Type', 'text/plain');
});

fs.readFile(__dirname + "/templates/index.html")
    .then(contents => {
        indexFile = contents;
        server.listen(port, hostname, () => {
            console.log(`Server is running on http://${hostname}:${port}`);
        });
    })
    .catch(err => {
        console.error(`Could not read index.html file: ${err}`);
        process.exit(1);
    });
