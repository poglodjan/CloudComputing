import React, { useEffect } from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  useLocation,
} from "react-router-dom";

import { AuthProvider } from "./context/AuthContext";

import Signup from "./components/Signup";
import About from "./components/About";
import Login from "./components/Login";
import Dashboard from "./components/Dashboard";
import PrivateRoute from "./components/PrivateRoute";
import Navbar from "./components/Navbar";
import Home from "./components/Home";
import Logout from "./components/Logout";
import CompleteProfile from "./components/CompleteProfile";
import ForgotPassword from "./components/ForgotPassword";
import StudentProfile from "./components/StudentProfile";
import Class from "./components/Class";
import ChildPage from "./components/ChildPage";

import PsychoSpherePage from "./psychosphere-pages/PsychoSpherePage";
import ArticlePage from "./psychosphere-pages/ArticlePage";
import SubscriptionPage from "./psychosphere-pages/SubscriptionPage";

import "./App.css";


function AppRoutes() {
  const location = useLocation();

  const isPsychosphereRoute =
    location.pathname.startsWith("/psychosphere");

  return (
    <>
      <Navbar />

      <main
        className={
          isPsychosphereRoute
            ? "app-content app-content--psychosphere"
            : "app-content app-content--default"
        }
      >
        <Routes>
          <Route path="/" element={<Home />} />

          <Route path="/signup" element={<Signup />} />

          <Route path="/about" element={<About />} />

          <Route
            path="/complete-profile"
            element={<CompleteProfile />}
          />

          <Route path="/login" element={<Login />} />

          <Route
            path="/dashboard"
            element={
              <PrivateRoute>
                <Dashboard />
              </PrivateRoute>
            }
          />

          <Route
            path="/psychosphere"
            element={<PsychoSpherePage />}
          />

          <Route
            path="/psychosphere/articles/:slug"
            element={<ArticlePage />}
          />

          <Route
            path="/psychosphere/subscription"
            element={<SubscriptionPage />}
          />

          <Route
            path="/forgot-password"
            element={<ForgotPassword />}
          />

          <Route path="/logout" element={<Logout />} />

          <Route path="/child" element={<ChildPage />} />

          <Route
            path="/students/:id"
            element={<StudentProfile />}
          />

          <Route
            path="/class"
            element={
              <Class>
                <Dashboard />
              </Class>
            }
          />
        </Routes>
      </main>
    </>
  );
}


function App() {
   

  return (
    <Router>
      <AuthProvider>
        <AppRoutes />
      </AuthProvider>
    </Router>
  );
}

export default App;