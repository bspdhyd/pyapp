let stream;

function startCamera() {
    const video = document.getElementById('video');
    const modalPreview = document.getElementById('modalPreview');
    const captureBtn = document.getElementById('captureBtn');
    const retakeBtn = document.getElementById('retakeBtn');

    video.style.display = 'block';
    modalPreview.style.display = 'none';
    captureBtn.style.display = 'inline-block';
    retakeBtn.style.display = 'none';

    navigator.mediaDevices.getUserMedia({ video: true })
        .then(function (mediaStream) {
            stream = mediaStream;
            video.srcObject = stream;
            const modal = new bootstrap.Modal(document.getElementById('cameraModal'));
            modal.show();
        })
        .catch(function (err) {
            alert("Could not access the camera. Error: " + err);
        });
}

function stopCamera() {
    if (stream) {
        stream.getTracks().forEach(track => track.stop());
        stream = null;
    }
}

function capturePhoto() {
    const video = document.getElementById('video');
    const modalPreview = document.getElementById('modalPreview');
    const canvas = document.createElement('canvas');
    canvas.width = 160;
    canvas.height = 120;

    const ctx = canvas.getContext('2d');
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    const imageDataUrl = canvas.toDataURL('image/jpeg');

    modalPreview.src = imageDataUrl;
    modalPreview.style.display = "block";
    video.style.display = "none";

    document.getElementById('captured_image').value = imageDataUrl;

    document.getElementById('captureBtn').style.display = 'none';
    document.getElementById('retakeBtn').style.display = 'inline-block';

    stopCamera();  // Stop stream after capturing
}

function retakePhoto() {
    startCamera();
}