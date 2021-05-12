
let captureData = [];

function removeCapture(){
    if(captureData.length > 0){
        captureData=[];
    }
    
}


function open_cam() {

    removeCapture();
    //document.getElementById("cap_btn").disabled = false; 
    var video = document.getElementById("video");


    navigator.mediaDevices.getUserMedia({
            video: true,
            audio: false,
        }).then(function (stream) {
            video.srcObject = stream;
        })
        .catch((error) => {
            console.log(error);
        })
}

function capture() {

    for (var i = 0; i < 30; i++) {

        var canvas = document.getElementById('canvas');
        var video = document.getElementById('video');
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        var ctx = canvas.getContext('2d');
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
        
        var photo = document.getElementById("canvas").toDataURL("image/png");
        photo = photo.replace(/^data:image\/(png|jpg);base64,/, "")
        // console.log(photo)
        captureData[i] = photo;
    }
    // console.log(captureData);
    
}


function sendData()
{

    const data = {frames: captureData};
    console.log(data);
    fetch("http://localhost:5000/check_image",{
        body: JSON.stringify(data),
        method: "POST",
        headers:{
            'Content-Type': 'application/json',
        }
    })
    .then(data => data.json())
    .then((result) => {
        console.log(result);
        window.location.href="/aadhar/" + result.id;
    })
    .catch((error) => {
        console.log(error);
    })
}