import express, { Request, Response } from "express";
import { Server } from "socket.io";
import http from "http";

const app = express();
const httpServer = http.createServer(app);
const server = new Server(httpServer);

app.use(express.static("public"));

server.on("connection", (socket) => {
  console.log("Client connected");

  socket.on("disconnect", () => {
    console.log("Client disconnected");
  });

  socket.on("message", (message) => {
    console.log(`Received message: ${message}`);
    socket.emit("message", `Server response: ${message}`);
  });
});

httpServer.listen(8080, () => {
  console.log("Server listening on port 3000");
});
