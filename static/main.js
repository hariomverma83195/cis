let home = window.location.origin;
let links = document.querySelectorAll(".side-nav li");
let ahrefs = ["/", "/clear", "/fromvid", "/clearadd", "/edit", "/add", "/delete", "/search", "/admin/settings", "/admin/users", "/admin/about"]
let userBtn = document.querySelector(".user-info");
let uploadBlur = document.querySelector("#uploadBlur");
let totalTime = parseInt(localStorage.getItem("totalTill"))
let totalOp = parseInt(localStorage.getItem("totalOp"))
let last = parseInt(localStorage.getItem("totalLastOperation"))

if(!localStorage.getItem("user")) {
    window.location.href = home + "/home"
}

for(let i=0; i<ahrefs.length; i++)
{
    links[i].addEventListener("click", () => {
        window.location.href = home+ahrefs[i];
    })
}

userBtn.addEventListener("click", function() {
    if(window.location.href != home+ahrefs[7]){
        window.location.href = home+ahrefs[7];
    }
})

// document.getElementById('personForm').addEventListener('submit', );

function submitFormFunction(event) {
        event.preventDefault();
    
        let formData = new FormData();
        formData.append('name', document.getElementById('name').value);
        formData.append('nicknames', document.getElementById('nicknames').value);
        formData.append('idMark', document.getElementById('idMark').value);
        formData.append('dob', document.getElementById('dob').value);
        formData.append('birthplace', document.getElementById('birthplace').value);
        formData.append('suspect', document.querySelector('input[name="suspect"]:checked').value);
        formData.append('explanation', document.getElementById('explaination').value);
        formData.append('image', document.getElementById('image').files[0]);
    
        fetch('/add_person', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (response.ok) {
                return response.json();
            }
            throw new Error('Network response was not ok.');
        })
        .then(data => {
            console.log(data);
            alert('Person added successfully');
            window.location.reload()
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
            alert('There was an error adding the person');
        });
}


function submitFormFunction2(event) {
    event.preventDefault();

    let formData = new FormData();
    formData.append('name', document.getElementById('name').value);
    formData.append('nicknames', document.getElementById('nicknames').value);
    formData.append('idMark', document.getElementById('idMark').value);
    formData.append('dob', document.getElementById('dob').value);
    formData.append('birthplace', document.getElementById('birthplace').value);
    formData.append('suspect', document.querySelector('input[name="suspect"]:checked').value);
    formData.append('explanation', document.getElementById('explaination').value);
    formData.append('file', document.getElementById('image').files[0]);

    fetch('/clear_add', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        }
        throw new Error('Network response was not ok.');
    })
    .then(data => {
        console.log(data);
        alert('Person added successfully');
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
        alert('There was an error adding the person');
    });
}

let uploadNonBlur = document.querySelector("#uploadNonBlurr")


uploadNonBlur.addEventListener("click", () => {
    document.getElementById("loading1").style.display = "flex";
    document.getElementById("content2").style.display = "none";
    // Assuming you have an input field with type="file" in your HTML with id="imageInput"
    const file = document.getElementById('uploadNonBlur').files[0];
    
    // Create a FormData object to store the file
    const formData = new FormData();
    formData.append('image', file);

    // Send a POST request to the /clear_image route with the FormData containing the image
    fetch('/verify_image', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to upload image');
        }
        return response.json();
    })
    .then(data => {
        console.log(data)
        if(data["imageName"] == "nomatch"){
            alert("No Match Found")
            window.location.reload()
        }else{
            window.location.href = home + "/match/" + data["imageName"];
        }
        console.log(data); // Log the response from the server
    })
    .catch(error => {
        console.error('Error:', error.message); // Log any errors
    });
});





function submitFormFunction3(event) {
    event.preventDefault();
    const formId = event.target.form.id;
    const formData = new FormData(document.getElementById(formId));
    let data = {};
    formData.forEach((value, key) => {
        data[key] = value;
    });

    data = {
        ...data,
        id: formId
    }

    fetch('/edit_record', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        }
        throw new Error('Network response was not ok.');
    })
    .then(data => {
        console.log(data);
        alert('Record updated successfully');
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
        alert('There was an error adding the person');
    });
}

uploadBlur.addEventListener("click", () => {
    document.getElementById("loading1").style.display = "flex";
    document.getElementById("content2").style.display = "none";
    // Assuming you have an input field with type="file" in your HTML with id="imageInput"
const file = document.getElementById('imageInputFile').files[0];
    
    // Create a FormData object to store the file
    const formData = new FormData();
    formData.append('image', file);

    // Send a POST request to the /clear_image route with the FormData containing the image
    fetch('/clear_image', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to upload image');
        }
        return response.json();
    })
    .then(data => {
        if(data["imageName"] == "nomatch"){
            alert("No Match Found")
            localStorage.setItem("totalTill", totalTime?(totalTime+parseInt(data["totalLastOperation"])):"00s");
            localStorage.setItem("lastOp", parseInt(data["totalLastOperation"]))
            localStorage.setItem("totalOp", parseInt(totalOp?totalOp+1:"01"))
            window.location.reload();
        }else{
            console.log(data)
            window.location.href = home + "/match/" + data["imageName"];
        }
        console.log(data); // Log the response from the server
    })
    .catch(error => {
        console.error('Error:', error.message); // Log any errors
    });
});