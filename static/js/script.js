document.addEventListener('DOMContentLoaded', function () {
    var ui = new firebaseui.auth.AuthUI(firebase.auth());

    ui.start('#firebaseui-auth-container', {
        callbacks: {
            signInSuccessWithAuthResult: function (authResult, redirectUrl) {
                console.log("logged in")
                return true;
            },
        },
        signInSuccessUrl: '/home.html',
        signInOptions: [
            firebase.auth.EmailAuthProvider.PROVIDER_ID
        ],
        // Other config options...
    });
});