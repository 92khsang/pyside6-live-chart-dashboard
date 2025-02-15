import { defineConfig } from "vite";
import { resolve } from "path";

export default defineConfig({
    root: "src",
    base: "./",
    resolve: {
        alias: {
            "@": resolve(__dirname, "src"),
        }
    },
    build: {
        outDir: "../../assets",
        emptyOutDir: true,
        rollupOptions: {
            input: {
                main: resolve(__dirname, "src", "index.html"),
            }
        }
    },
    server: {
        port: 3000
    }
});
