import { BrowserRouter as Router, Routes, Route } from "react-router-dom"; /*its element of SPAd type apps*/
import { AuthProvider } from "./context/AuthContext";
import Signup from "./components/Signup";
import About from "./components/About";
import Login from "./components/Login";
import Dashboard from "./components/Dashboard";
import PrivateRoute from "./components/PrivateRoute";
import Navbar from "./components/Navbar";
import Home from "./components/Home";
import PsychoSphere from "./components/PsychoSphere";
import Logout from "./components/Logout";
import CompleteProfile from "./components/CompleteProfile";
import './App.css'
import ForgotPassword from "./components/ForgotPassword";
import React, { useEffect } from 'react';
import StudentProfile from "./components/StudentProfile"; 
import Class from "./components/Class";
import ChildPage from "./components/ChildPage";
import PsychoSpherePage from "./psychosphere-pages/PsychoSpherePage";
import ArticlePage from "./psychosphere-pages/ArticlePage";
import SubscriptionPage from "./psychosphere-pages/SubscriptionPage";

function App() {
  useEffect(() => {
    fetch("http://localhost:8000/api/hello/")
      .then((res) => res.json())
      .then((data) => console.log("API response:", data))
      .catch((err) => console.error("API error:", err)); // it checks if CORS work and if we have connected backend with react, yes we have!
  }, []);
  return (
    <AuthProvider>
      <Router>
        <Navbar></Navbar>
        <Routes>
          <Route path="/" element={<Home />}></Route>
          <Route path="/signup" element={<Signup />} />
          <Route path="/about" element={<About />} />
          <Route path="/complete-profile" element={<CompleteProfile />} />
          <Route path="/login" element={<Login />} />
          <Route path="/dashboard" element={<PrivateRoute><Dashboard /></PrivateRoute>} />
          <Route
            path="/psychosphere"
            element={<PsychoSpherePage />}
          />

          <Route
            path="/psychosphere/articles/:slug"
            element={<ArticlePage />}
          />
          <Route path="/forgot-password" element={<ForgotPassword />} />
          <Route path="/Logout" element={<Logout />} />
          <Route path="/child" element={<ChildPage />} />
          <Route path="/students/:id" element={<StudentProfile />} />
          <Route path="/class" element={<Class><Dashboard /></Class>} />
          <Route
            path="/psychosphere/subscription"
            element={<SubscriptionPage />}
          />
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;
