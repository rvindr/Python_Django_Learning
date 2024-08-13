const loginForm = document.getElementById("login-form")
const baseEndPoint = 'http://localhost:8000/api'
const registerForm = document.getElementById("register-form")
const registerMsg = document.getElementById("register-msg")
const contentContainer = document.getElementById("blog-container")

if (loginForm) {
    loginForm.addEventListener('submit', handleLogin)
}

function handleLogin(event) {
    // console.log(event)
    event.preventDefault()
    const loginEndpoint = `${baseEndPoint}/token/`
    // console.log(loginEndpoint)
    let loginFormData = new FormData(loginForm) // FromData is built-in class 
    let loginObjectData = Object.fromEntries(loginFormData)
    let bodyStr = JSON.stringify(loginObjectData)
    // console.log(bodyStr)
    const options = {
        method: "POST",
        headers : {
            "Content-Type" : "application/json"
        },
        body : bodyStr
    }
    fetch(loginEndpoint, options)
    .then(
        response =>{
            console.log(response)
            return response.json()
        })
        .then(authData=>{
            handleAuthData(authData, getBlog)

        })
        .catch(err=>{
            console.log(err)
        })
}

function handleAuthData(authData, callback){
    localStorage.setItem("Access",authData.access)
    localStorage.setItem("Refresh",authData.refresh)
    // window.location.href = 'http://localhost:8000/client-blog/';
    if (callback){
        callback()
    }
}
function writeToContainer(data){
    if (contentContainer){
        contentContainer.innerHTML = `<pre> ${JSON.stringify(data, null, 4)} </pre>`
    }
}
function getBlog(){
    const blogEndpoint = `${baseEndPoint}/blog-post/`
    options ={
        method : "GET",
        headers : 
        {
            "Content-Type":"application/json",
            "Authorization" : `Bearer ${localStorage.getItem("Access")}`
        }
    }
    fetch(blogEndpoint,options)
    .then(response=>response.json())
    .then(data=>{
        console.log(data)
        writeToContainer(data)
    })
}








if (registerForm){
    registerForm.addEventListener('submit', handleRegister)
}


function getCSRFToken() {
    let csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    return csrfToken;
}
function handleRegister(event){
    event.preventDefault()
    const registerEndpoint = `${baseEndPoint}/register/`
    let registerFormData = new FormData(registerForm)
    let registerObjectData = Object.fromEntries(registerFormData)
    let bodyStr = JSON.stringify(registerObjectData)
    console.log(bodyStr)
    options = {
        method : "POST",
        headers : {
            "Content-Type" : "application/json",
            "X-CSRFToken": getCSRFToken()
        },
        body : bodyStr
    }

    fetch(registerEndpoint, options)
    .then(response=>{
        console.log(response)
        return response.json()
    })
    .then(data=>{
        showMessage(data)
    })
    .catch(err=>{
        console.log(err)
    })

}

function showMessage(data){
    registerForm.innerHTML = `<div class="alert alert-success" role="alert">
  ${data.message}
</div>`
}


