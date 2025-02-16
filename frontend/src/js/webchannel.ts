// @ts-nocheck
export class WebChannelHandler {
    private static instance: WebChannelHandler;
    private handler: any;
    private callbacks: Map<string, (msg: string) => void> = new Map();
    private isReady: boolean = false;
    private onReady: Promise<void>;

    private constructor() {
        this.onReady = new Promise<void>((resolve) => {
            this.loadQWebChannel().then(() => {
                this.setupWebChannel();
                resolve();  // Mark WebChannel as ready
            });
        });
    }

    public static getInstance(): WebChannelHandler {
        if (!WebChannelHandler.instance) {
            WebChannelHandler.instance = new WebChannelHandler();
        }
        return WebChannelHandler.instance;
    }

    private async loadQWebChannel() {
        if (typeof QWebChannel === "undefined") {
            await new Promise<void>((resolve, reject) => {
                const script = document.createElement("script");
                script.src = "qrc:///qtwebchannel/qwebchannel.js";
                script.onload = () => resolve();
                script.onerror = () => reject(new Error("Failed to load qwebchannel.js"));
                document.head.appendChild(script);
            });
        }
    }

    private setupWebChannel() {
        new QWebChannel(qt.webChannelTransport, (channel) => {
            this.handler = channel.objects.handler;
            this.isReady = true;

            if (!this.handler) {
                console.error("WebChannel handler is undefined!");
                return;
            }

            if (this.handler.setup_translate_py2js) {
                this.handler.setup_translate_py2js((channelName: string, msg: string) => {
                    if (!channelName || channelName.trim() === "") {
                        console.warn(`Received a message with an empty channel: ${msg}`);
                        return;
                    }
                    this.dispatchMessage(channelName, msg);
                });
            } else {
                console.error("WebChannel handler is missing setup_translate_py2js method!");
            }
        });
    }

    private dispatchMessage(channelName: string, msg: string) {
        const callback = this.callbacks.get(channelName);
        if (callback) {
            callback(msg);
        } else {
            console.warn(`No callback registered for channel '${channelName}'`);
        }
    }

    public async registerCallback(channelName: string, callback: (msg: string) => void) {
        await this.onReady;  // Wait for WebChannel to be ready before registering
        this.callbacks.set(channelName, callback);
    }

    public async sendMessage(channelName: string, message: string) {
        await this.onReady;  // Ensure WebChannel is ready before sending
        if (this.handler) {
            if (this.handler.translate_js2py) {
                this.handler.translate_js2py(channelName, message);
            } else {
                console.error("WebChannel handler is missing translate_js2py method!");
            }
        } else {
            console.error("WebChannel is not initialized yet.");
        }
    }
}
