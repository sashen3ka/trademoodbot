import { initializeApp } from "firebase/app";
import { getFirestore } from "firebase/firestore";

const firebaseConfig = {
  apiKey: "AIzaSyAcJSSMIWBYJNnXkdZTbjwcKIUv2I_HdV4",
  authDomain: "trademoodbot.firebaseapp.com",
  projectId: "trademoodbot",
  storageBucket: "trademoodbot.firebasestorage.app",
  messagingSenderId: "466666247386",
  appId: "1:466666247386:web:a41b794e78120875af01e3",
  measurementId: "G-S95SHZJ6DL"
};

const app = initializeApp(firebaseConfig);
const db = getFirestore(app); // ← вот этой строки не хватало

export { db };
