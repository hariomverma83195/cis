let loginDiv = document.querySelector("#logindiv")
let signupDiv = document.querySelector("#sigupdiv")

let loginBtn = document.querySelector("#loginBtn")
let signupBtn = document.querySelector("#signupBtn")

let cancelBtn = document.querySelectorAll(".cancelBtn")

function loginFun() {
    loginDiv.style.display = "flex"
}

function signupFun(){
    console.log("Nnn")
    signupDiv.style.display = "flex"
}

cancelBtn[0].addEventListener("click", () => {
    loginDiv.style.display = "none"
})

cancelBtn[1].addEventListener("click", () => {
    signupDiv.style.display = "none"
})


function login(event) {
    event.preventDefault();
    const formData = new FormData(document.getElementById('loginForm'));
    const data = {};
    formData.forEach((value, key) => {
        data[key] = value;
    });

    fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        if(data.message != ''){
            localStorage.setItem("user", data.message)
            window.location.href = window.location.origin
        }else{
        alert(data.message);
        }
        // Redirect to dashboard or another page after successful login
        // window.location.href = '/dashboard';
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Invalid email or password');
    });
}


function signup(event) {
    event.preventDefault()
    const formData = new FormData(document.getElementById('signupForm'));
    const data = {};
    formData.forEach((value, key) => {
        data[key] = value;
    });

    fetch('/signup', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        windows.location.href = "/";
    })
    .catch(error => console.error('Error:', error));
}