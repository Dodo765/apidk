const express = require("express");
const path = require("path");
const fs = require("fs");
const app = express();
const bodyParser = require("body-parser");
const { exec } = require("child_process");

// Server port
const PORT = 3000;

function log(message) {
	// Pobierz aktualną datę i czas
	const now = new Date();
	// Pobierz poszczególne elementy daty i czasu
	const year = now.getFullYear();
	const month = String(now.getMonth() + 1).padStart(2, "0");
	const day = String(now.getDate()).padStart(2, "0");
	const hour = String(now.getHours()).padStart(2, "0");
	const minute = String(now.getMinutes()).padStart(2, "0");
	const second = String(now.getSeconds()).padStart(2, "0");
	// Utwórz pełny format wiadomości z datą i czasem
	const formattedMessage = `[${year}-${month}-${day} ${hour}:${minute}:${second}] ${message}`;
	// Wyświetl sformatowaną wiadomość w konsoli
	console.log(formattedMessage);
}

app.get("/", (request, response) => {
	log(request.url);
	response.send("TEST");
	response.status(200);
});
app.get("/tallyLight/firmware/firmware.bin", (request, response) => {
	log(request.url);
	response.download(path.join(__dirname, "/tallyLight/firmware/firmware.bin"), "firmware.bin", (err) => {
		if (err) {
			console.error("Problem on download firmware: ", err);
		}
	});
});

app.get("/tallyLight/firmware/version", (request, response) => {
	log(request.url);
	try {
		const versionPath = path.join(__dirname, "/tallyLight/firmware/version.txt");
		const versionContent = fs.readFileSync(versionPath, "utf8");

		response.send(versionContent);
		response.status(200);
	} catch (err) {
		console.error("Problem reading version.txt: ", err);
		response.status(500).send("Internal Server Error");
	}
});

//Datavideo
app.get("/datavideo/firmware/firmware.bin", (request, response) => {
	log(request.url);
	response.download(path.join(__dirname, "/datavideo/firmware/firmware.bin"), "firmware.bin", (err) => {
		if (err) {
			console.error("Problem on download firmware: ", err);
		}
	});
});

app.get("/datavideo/firmware/version", (request, response) => {
	log(request.url);
	try {
		const versionPath = path.join(__dirname, "/datavideo/firmware/version");
		const versionContent = fs.readFileSync(versionPath, "utf8");

		response.send(versionContent);
		response.status(200);
	} catch (err) {
		console.error("Problem reading version: ", err);
		response.status(500).send("Internal Server Error");
	}
});

app.get("/jdownloader", (req, res) => {
	const versionPath = path.join(__dirname, "/index.html");
	res.send(fs.readFileSync(versionPath, "utf8"));
	res.status(200);
});

app.use(express.static("public"));

app.all("*", (req, res) => {
	log(req.url);
	res.status(404);
	res.json({ status: "Not Found" });
	res.end();
});

app.listen(PORT, "0.0.0.0", () => {
	console.log("serving on: http://api.dominikkawalec.pl:3000/tallyLight/firmware/version");
});
