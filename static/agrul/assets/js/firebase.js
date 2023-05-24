// Import the functions you need from the SDKs you need
import { initializeApp } from "https://www.gstatic.com/firebasejs/9.18.0/firebase-app.js";
import { getAnalytics } from "https://www.gstatic.com/firebasejs/9.18.0/firebase-analytics.js";
import { getDatabase, ref, set, onValue } from 'https://www.gstatic.com/firebasejs/9.18.0/firebase-database.js'
// import { getDatabase, ref, set, onValue } from "firebase/database";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
    apiKey: "AIzaSyDhRNN_WWyWszxTvkSW_lK-NBwV-YUvEZw",
    authDomain: "discuzz-41e23.firebaseapp.com",
    databaseURL: "https://discuzz-41e23-default-rtdb.firebaseio.com",
    projectId: "discuzz-41e23",
    storageBucket: "discuzz-41e23.appspot.com",
    messagingSenderId: "1095873107128",
    appId: "1:1095873107128:web:ddc8912b8a968e3837104d",
    measurementId: "G-6W9WX0Q960"
  };
// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);

export function writeToFirebase(message) {
    const db = getDatabase(app);
    const reference = ref(db, `/private-messages/`)
    set(reference, message)
}

export function listenOnFirebaseMessages(printNewMessageToChat) {
    const db = getDatabase(app);
    const reference = ref(db, `/private-messages/`)
    onValue(reference, (snapshot) => {
        const data = snapshot.val();
        console.log("Last message: ", data)
        printNewMessageToChat(data, false)
    })
}


export function writeToFirebaseGroup(message) {
    const db = getDatabase(app);
    const reference = ref(db, `/groups/messages/`)
    set(reference, message)
}

export function listenOnFirebaseGroupMessages(printNewMessageToChat) {
    const db = getDatabase(app);
    const reference = ref(db, `/groups/messages/`)
    onValue(reference, (snapshot) => {
        const data = snapshot.val();
        printNewMessageToChat(data, true)
    })
}
