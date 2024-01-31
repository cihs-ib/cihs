var firebaseConfig = 
                { 
                    apiKey: "AIzaSyBV3a_le3dYt4F7SwvcEccfWXwF_IGUba4",
                    authDomain: "uqhs-62406.firebaseapp.com",
                    databaseURL: "https://uqhs-62406-default-rtdb.firebaseio.com",
                    projectId: "uqhs-62406",
                    storageBucket: "uqhs-62406.appspot.com",
                    messagingSenderId: "636403912195",
                    appId: "1:636403912195:web:1932ccc97c70f63357c836",
                    measurementId: "G-8TDX392M7W" 
                }; // Initialize Firebase 
                firebase.initializeApp(firebaseConfig); 
         //invokes firebase authentication. 
                const auth = firebase.auth(); 
                        /*something here */
                const register = () => { 
                        const bio = document.querySelector("#lname").value; +' '+document.querySelector("#fname").value;;
                        const email = document.querySelector("#registration-email").value; 
                        const reemail = document.querySelector("#registration-reemail").value; 
                        const password1 = document.querySelector("#registration-password1").value;
                        const password2 = document.querySelector("#registration-password2").value; 
                            if (email.trim() == "") { alert("Enter Email"); } 
                            else if (password1.trim().length < 7) { 
                                alert("Password must be at least 7 characters"); } 
                            else if (email != reemail) { alert("emails do not match"); }
                            else if (password1 != password2) { alert("password do not match"); }
                            else if (bio == "" || bio.trim().length < 7) { alert("please enter User Name!"); }
                            else { 
                                var password = password1;
                                auth.createUserWithEmailAndPassword(email, password).catch(function (error){ 
                                                // Handle Errors here. 
                                    var errorCode = error.code; 
                                    var errorMessage = error.message; alert(errorMessage); 
                                         
                                            }).then(function(){
                                              
                                          const auth = firebase.auth(); 
                                            auth.signInWithEmailAndPassword(email, password); 
                                            firebase.auth().signInWithEmailAndPassword(email, password).catch(function (error) { // Handle Errors here. 
                                      var errorCode = error.code; 
                                      var errorMessage = error.message; 
                                      alert(errorMessage); });
                                      var userNow = firebase.auth().currentUser;
                                        userNow.updateProfile({
                                        displayName:bio
                                      }).then(function() {
                                        localStorage.setItem('displayName', userNow.displayName);
                                        var oldurl = document.referrer;
                                            location.replace(oldurl)
                                      }, function(error) {
                                        console.log(error)
                                      });}); 
                                             ;} };
                            document.querySelector("#register").addEventListener("click", () => { register(); }); 
                                            //register when you hit the enter key 
                            if (document.querySelector("#registration-password")){
                                document.querySelector("#registration-password").addEventListener("keyup", (e) => { 
                                    if (event.keyCode === 13) { e.preventDefault(); register(); } });
                            } 
                        const login = () => { 
                        const email = document.querySelector("#login-email").value; 
                        const password = document.querySelector("#login-password").value; 
                            if (email.trim() == "") { alert("Enter Email"); } 
                            else if (password.trim() == "") { alert("Enter Password"); } 
                            else { authenticate(email, password); 
                              } }; 
                            document.querySelector("#login").addEventListener("click", () => { login(); }); 
                                            //sign in when you hit enter 
                            document.querySelector("#login-password").addEventListener("keyup", (e) => { 
                                    if (event.keyCode === 13) { e.preventDefault(); login(); } }); 
                                            const authenticate = (email, password) => { 
                                                const auth = firebase.auth(); 
                                                auth.signInWithEmailAndPassword(email, password); 
                                                firebase.auth().signInWithEmailAndPassword(email, password).catch(function (error) { // Handle Errors here. 
                                                    var errorCode = error.code; 
                                                    var errorMessage = error.message; alert(errorMessage); }).then(function() {
                                                      var userNow = firebase.auth().currentUser;
                                                      localStorage.setItem('uid', userNow.uid);
                                                      localStorage.setItem('displayName', userNow.displayName);
                                                      var oldurl = document.referrer;
                                                          location.replace(oldurl)
                                                      }, function(error) {
                                                        console.log(error)
                                                      }); }; 
                                                    /*something here  location.reload(); */
                                                    document.querySelector("#out").addEventListener("click", () => { firebase.auth().signOut().then(function () {$('#log-outs').hide();}).catch(function (error) { 
                                                        alert("error signing out, check network connection"); }).then(function() {localStorage.setItem('displayName', '')});
                                                        
                                                         }); 
                                                        auth.onAuthStateChanged((firebaseUser) => { 
                                                            if (firebaseUser) { 
                                                              $('#signin').hide();
                                                              $('#loginStatus').show()
                                                              $('#loginStatus').html('You are logged in as '+localStorage.getItem('displayName')) } }); 
                                                            document.querySelector("#forgot-password").addEventListener("click", () => { 
                                                                const email = document.querySelector("#login-email").value; 
                                                                if (email.trim() == "") { alert("Enter Email"); } 
                                                                else { forgotPassword(email); } }); 
                                                                const forgotPassword = (email) => { 
                                                                    auth.sendPasswordResetEmail(email).then(function () { 
                                                                        alert("A password reset email has been sent to "+ ' '+email); }).catch(function (error) { alert("invalid email or bad network connection"); }); }; 
