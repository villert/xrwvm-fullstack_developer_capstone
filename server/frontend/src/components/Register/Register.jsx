import React, { useState } from "react";
import Header from "../Header/Header";
import "./Register.css";
import person from "../assets/person.png";
import email from "../assets/email.png";
import passwordIcon from "../assets/password.png";

const Register = () => {
  const [userName, setUserName] = useState("");
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [emailAddress, setEmailAddress] = useState("");
  const [password, setPassword] = useState("");

  const register = async (e) => {
    e.preventDefault();

    const res = await fetch(`${window.location.origin}/djangoapp/register`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        userName,
        firstName,
        lastName,
        email: emailAddress,
        password,
      }),
    });

    const json = await res.json();
    if (json.status === "User created") {
      sessionStorage.setItem("username", userName);
      sessionStorage.setItem("firstname", firstName);
      sessionStorage.setItem("lastname", lastName);
      window.location.href = "/";
    } else {
      alert(json.message || "The user could not be registered.");
    }
  };

  return (
    <div>
      <Header />
      <form className="register_container" onSubmit={register}>
        <div className="header">Sign Up</div>
        <div className="inputs">
          <div className="input">
            <img src={person} className="img_icon" alt="Username" />
            <input className="input_field" type="text" placeholder="Username" value={userName} onChange={(e) => setUserName(e.target.value)} required />
          </div>
          <div className="input">
            <img src={person} className="img_icon" alt="First name" />
            <input className="input_field" type="text" placeholder="First Name" value={firstName} onChange={(e) => setFirstName(e.target.value)} required />
          </div>
          <div className="input">
            <img src={person} className="img_icon" alt="Last name" />
            <input className="input_field" type="text" placeholder="Last Name" value={lastName} onChange={(e) => setLastName(e.target.value)} required />
          </div>
          <div className="input">
            <img src={email} className="img_icon" alt="Email" />
            <input className="input_field" type="email" placeholder="Email" value={emailAddress} onChange={(e) => setEmailAddress(e.target.value)} required />
          </div>
          <div className="input">
            <img src={passwordIcon} className="img_icon" alt="Password" />
            <input className="input_field" type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} required />
          </div>
        </div>
        <div className="submit_panel">
          <button className="submit" type="submit">Register</button>
        </div>
      </form>
    </div>
  );
};

export default Register;
