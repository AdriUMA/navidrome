var lastId = null;
var updating = false;

async function update() {
    while(true) {
        await sleep(2000);
        if (!lastId || updating) continue;
        await statusChecker(lastId);
    }
}
update();

async function requestDownload() {
    const url = document.getElementById("urlInput").value;
    const message = document.getElementById("message");

    message.style.color = "inherit";

    if (!url.trim()) {
        message.textContent = "Por favor, introduce una URL.";
        return;
    }

    message.textContent = "Procesando...";

    try {
        const res = await fetch("http://localhost:8000/download", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ url })
        });

        const minWait = sleep(200);
        const data = await res.json();
        await minWait;

        if (res.ok) {
            message.textContent = `Preparando... ID: ${data.id}`;
            await sleep(2000);
            lastId = data.id;
            statusChecker(lastId);
        } else {
            message.textContent = `Error: ${data.detail || "desconocido"}`;
            message.style.color = "red";
        }
    } catch (err) {
        message.textContent = "Error al conectar con el servidor.";
        message.style.color = "red";
    }
}

async function statusChecker(uuid) {
    updating = true;

    try {
    const res = await fetch(`http://localhost:8000/status/${uuid}`, {
            method: "GET",
            headers: { "Content-Type": "application/json" },
        });

        const data = await res.json();

        if (res.ok) {
            if (data.status == "processing") {
                message.textContent = `En proceso. ID: ${data.id}`;
                message.color = "green";
            } else if(data.status == "done") {
                message.textContent = `Completado.`;
                lastId = null;
                message.color = "green";
            }else {
                message.textContent = `Error: ${data.status || "desconocido"}`;
                lastId = null;
                message.style.color = "red";
            }
        } else {
            message.textContent = `Error: ${data.detail || "desconocido"}`;
            lastId = null;
            message.style.color = "red";
        }
    } catch (err) {
        message.textContent = "Error al conectar con el servidor.";
        lastId = null;
        message.style.color = "red";
    }
    finally{
        updating = false;
    }
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}