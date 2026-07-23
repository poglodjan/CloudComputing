import React from "react";
import { NavLink } from 'react-router-dom';
import { useAuth } from "../context/AuthContext"; // Import the custom hook
import "./Navbar.css"; // Import CSS for styling

const Navbar = () => {
console.log("Navbar is rendering...");
const { user, role } = useAuth();
console.log("User:", user);
console.log("Role:", role);
  return (
      <nav className="navbar">
          <div className="logo">Neurodetective</div>

          <div className="nav-sections">
              <ul className="nav-NavLinks">
                  <li><NavLink to="/">Home</NavLink></li>
                  <li><NavLink to="/about">About Us</NavLink></li>
                  <li><NavLink to="/psychosphere">PsychoSphere</NavLink></li>

                  {role === "student" && (
                      <>
                          <li><NavLink to="/my-humor">My Humor</NavLink></li>
                          <li><NavLink to="/games">Games</NavLink></li>
                      </>
                  )}
                  {role === "parent" && (
                      <li><NavLink to="/child">Child</NavLink></li>
                  )}
                  {role === "teacher" && (
                    <>
                        <li><NavLink to="/class">Class</NavLink></li>
                        <li>
                        <a
                            href="https://docs.google.com/forms/d/e/1FAIpQLSfQPTijbJQb-Ub7jHNwXllJeNit5hWAWKV3l419yirSqU7lNw/viewform?usp=header"
                            target="_blank"
                            rel="noopener noreferrer"
                        >
                            Ankieta ADHD
                        </a>
                        </li>
                        <li>
                        <a
                            href="https://docs.google.com/forms/d/e/1FAIpQLSe_l78ywiA2-ZGNTUjMQSabHaReDtoxR8QZ2FPSvLIsx1FTEg/viewform?usp=header"
                            target="_blank"
                            rel="noopener noreferrer"
                        >
                            Ankieta Autyzmu
                        </a>
                        </li>
                    </>
                )}

              </ul>

              <div className="logout-section">
                  {user ? (
                      <NavLink to="/logout" className="logout-button">Logout</NavLink>
                  ) : (
                      <NavLink to="/login">Login/Register</NavLink>
                  )}
              </div>
          </div>
      </nav>
  );
};

export default Navbar;
