import {defineConfig} from "vite";
import {resolve} from "path";

export default defineConfig({
    root: "src",
    base: "./",
    resolve: {
        alias: {
            "@": resolve(__dirname, "src"),
        }
    },
    build: {
        outDir: "../../static",
        emptyOutDir: true,
        rollupOptions: {
            input: {
                editor: resolve(__dirname, "src", "html", "editor.html"),
                preview: resolve(__dirname, "src", "html", "chart.html")
            }
        }
    },
    server: {
        port: 3000
    }
});
