let camera_button = document.querySelector("#start-camera");
let video = document.querySelector("#video");
let click_button = document.querySelector("#click-photo");
let canvas = document.querySelector("#canvas");
let dataurl = document.querySelector("#dataurl");
let data_container = document.querySelector("#data-container");

let loadFile = function(event) {
    let reader = new FileReader();
    reader.readAsDataURL(event.target.files[0]);
    reader.onloadend = function (event) {
        let myImage = new Image();
        myImage.src = event.target.result;
        myImage.onload = function(ev) {
            canvas.getContext("2d").drawImage(myImage, 0, 0, canvas.width, canvas.height); // Draws the image on canvas
            let imgData = canvas.toDataURL("image/jpeg"); // Assigns image base64 string in jpeg format to a variable
            dataurl.value = imgData;
            sendData();
            data_container.style.display = 'block';
         }
    }   
}

camera_button.addEventListener('click', async function() {
    if(camera_button.innerHTML == 'Camera') {
        let stream = null;
        try {
            stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'user' }, audio: false });
        }
        catch(error) {
            alert(error.message);
            return;
        }

        video.srcObject = stream;
        camera_button.innerHTML = 'Stop Camera';
        video.style.display = 'block';
        click_button.style.display = 'block';
        data_container.style.display = 'none';
    } else {
        video.style.display = 'none';
        camera_button.innerHTML = 'Camera';
        click_button.style.display = 'none';
        video.pause();
        video.src = "";
        video.srcObject.getTracks()[0].stop()
    }

});

click_button.addEventListener('click', function() {
    canvas.getContext('2d').drawImage(video, 0, 0, canvas.width, canvas.height);
    let image_data_url = canvas.toDataURL('image/jpeg');
    
    dataurl.value = image_data_url;
    sendData();
    data_container.style.display = 'block';

    video.style.display = 'none';
    camera_button.innerHTML = 'Camera';
    click_button.style.display = 'none';

    video.pause();
    video.src = "";
    video.srcObject.getTracks()[0].stop()
});

function sendData() {
    $.ajax({
        url: '/process',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ 'value': dataurl.value }),
        success: function(response){
            document.getElementById('value').innerHTML = response['value'];
        },
        error: function(error) {
            console.log(error);
        }
    });
}
