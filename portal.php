<?php
?>

<html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Portal - Astro</title>
    
        <style>
            body {
                font-family: Verdana, sans-serif;
                background-color: #000000;
                color: #EBD7FF;
                margin: 0;
            }
            h1 {
                font-size: 72px;
                margin: 0;
            }
            h2 {
                font-size: 24px;
                margin: 0;
            }
            .container {
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }
            .alignment-container{
                display: flex;
                flex-direction: row;
            }
            .branding-box{
                margin-right: 50px;
            }
            .name-and-icon {
                display: flex;
                align-items: center;
            }
            .name-and-icon svg {
                margin-right: 10px;
            }
            .form-container {
                display: flex;
                flex-direction: column;
                align-items: center;
            }
            form {
                margin: 0;
            }
            .sign-in {
                text-align: center;
                margin-left: 0;
            }
            .sign-in input {
                width: 100%;
                padding: 10px;
                margin-bottom: 10px;
                border-radius: 5px;
                font-family: inherit;
                background-color: #EBD7FF;
            }
            .sign-in input::placeholder {
                color: #000000;
            }
            .sign-in button {
                width: 100%;
                background-color: #972FFF;
                color: #EBD7FF;
                border: none;
                border-radius: 5px;
                padding: 10px;
                cursor: pointer;
                font-family: inherit;
                font-weight: bold;
            }
            .sign-up {
                color: #EBD7FF;
                text-align: center;
            }
            .sign-up a {
                color: #972FFF;
                font-weight: bold;
            }
        </style>
    </head>
    
    <body>
        <div class="container">
            <div class="alignment-container">
                <div class="branding-box">
                    <div class="name-and-icon">
                        <svg xmlns="http://www.w3.org/2000/svg" width = "72" height = "72" viewBox = "0 0 24 24" fill = "none"
                             stroke = "currentColor" stroke-width = "2" stroke-linecap = "round" stroke-linejoin = "round"
                             class = "icon icon-tabler icons-tabler-outline icon-tabler-moon-stars">
                            <path stroke = "none" d = "M0 0h24v24H0z" fill = "none"/>
                            <path d = "M12 3c.132 0 .263 0 .393 0a7.5 7.5 0 0 0 7.92 12.446a9 9 0 1 1 -8.313 -12.454z"/>
                            <path d = "M17 4a2 2 0 0 0 2 2a2 2 0 0 0 -2 2a2 2 0 0 0 -2 -2a2 2 0 0 0 2 -2"/>
                            <path d="M19 11h2m-1 -1v2" /></svg>
                        <h1>Astro</h1>
                    </div>
                    <h2>Your cosmic community.<br>Embark on cosmic conversations!</h2>
                </div>

                <div class="form-container">
                    <div class="sign-in">
                        <form method="post">
                            <input type="text" name="username" placeholder="Username" required>
                            <input type="password" name="password" placeholder="Password" required>
                            <button type="submit">Login</button>
                        </form>
                    </div>

                    <div class="sign-up">
                        <p>Don't have an account? <a href="signup.php">Sign Up</a></p>
                    </div>
                </div>
            </div>
        </div>
    </body>
</html>
