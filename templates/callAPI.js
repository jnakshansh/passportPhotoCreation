// import Cropper from 'cropperjs';

// const cropper = new cropper('#imageInput');

// const video_feed = document.getElementById('video-feed');
// const captureBtn = document.getElementById('capture-btn');
// const retakeBtn = document.getElementById('retake-btn');
const saveBtn = document.getElementById('save-btn');
const saveImagesBtns = document.getElementById('save-images-btns')
const capturedImage = document.getElementById('captured-image');
const header = document.getElementById('header');
const capturedImageContainer = document.getElementById('captured-image-container');
const uploadBtn = document.getElementById('upload-btn');
let cropperImage = document.getElementById('cropper-image');
const previewButton = document.getElementById("preview");
const previewImage = document.getElementById("preview-image");
let downloadButton = document.getElementById("download");
const croppedNumberOfImage = document.getElementById("croppedNumberOfImages");
let cropper = "";

// captureBtn.addEventListener('click', capturePhoto);
// retakeBtn.addEventListener('click', retakePhoto);
saveBtn.addEventListener('click', savePhoto);
uploadBtn.addEventListener('click', uploadImage);

// function capturePhoto() {
//     fetch('/capture_photo', {
//         method: 'POST',
//     })
//     .then(response => {
//         if (response.ok) {
//             updateCapturedImage();
//             retakeBtn.style.display = 'inline-block';
//             saveBtn.style.display = 'inline-block';
//         }
//     })
//     .catch(error => console.error('Error:', error));
// }

// function updateCapturedImage() {
//     fetch('/get_captured_image')
//     .then(response => response.text())
//     .then(imageData => {
//         if (imageData) {
//             capturedImage.style.display = 'block';
//             capturedImage.src = `data:image/jpeg;base64,${imageData}`;
//         } else {
//             capturedImage.style.display = 'none';
//         }
//     })
//     .catch(error => console.error('Error:', error));
//     // video_feed.style.display = 'none';
// }

function uploadImage(){
    var fileInput = document.getElementById('imageInput');
    var file = fileInput.files[0];
    
    var formData = new FormData();
    formData.append('image', file);

    fetch('/upload_image', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        if(data.image_base64){
            capturedImage.style.display = 'block';
            capturedImage.src = `data:image/jpeg;base64,${data.image_base64}`;
            saveBtn.style.display = 'inline-block';
        }
        else {
            capturedImage.style.display = 'none';
        }
        // Optionally, you can add additional functionality here based on the API response
    })
    .catch(error => console.error('Error:', error));

    
    let reader = new FileReader();
    reader.readAsDataURL(fileInput.files[0]);
    reader.onload = () => {
        cropperImage.setAttribute("src", reader.result);
        if(cropper){
            cropper.destroy();
        }
        cropper = new Cropper(cropperImage);
        previewButton.classList.remove("hide");
    };
    header.classList.remove("hide");
}

previewButton.addEventListener("click", (e) => {
    e.preventDefault();
    saveImagesBtns.classList.add("hide");
    downloadButton.classList.remove("hide");
    croppedNumberOfImage.classList.remove("hide");
    let imgSrc = cropper.getCroppedCanvas({}).toDataURL();
    //Set preview
    previewImage.src = imgSrc;
    // downloadButton.download = `cropped_image.png`;
    // downloadButton.setAttribute("href", imgSrc);
});

downloadButton.addEventListener("click", (e) => {
    e.preventDefault();
    imgSrc = cropper.getCroppedCanvas({}).toDataURL();
    var numberofImages = document.getElementById('croppedNumberOfImages').value;
    fetch('/save_cropped_image', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ imgSrc: imgSrc, numberOfImages: numberofImages }),
    })
    .then(response => response.text())
    .then(data => {console.log('Success:', data);})
    .catch((error) => {console.error('Error:', error);});

})

// function retakePhoto() {
//     // video_feed.style.display = 'block'
//     capturedImage.style.display = 'none';
//     retakeBtn.style.display = 'none';
//     saveBtn.style.display = 'none';
// }

function savePhoto() {
    // video_feed.style.display = 'none';
    var numberofImages = document.getElementById('numberOfImages').value;
    fetch('/save_image', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ numberOfImages: numberofImages })
    })
    .then(response => response.text())
    .then(message => {
        console.log(message);
        // Optionally, you can add additional functionality here, such as displaying a success message or redirecting to another page.
    })
    .catch(error => console.error('Error:', error));
}