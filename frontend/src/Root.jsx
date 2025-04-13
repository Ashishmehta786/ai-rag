import React, { useContext, useEffect } from "react";
import Navbar from "./components/Navbar";
import Hero from "./components/Hero";
import Features from "./components/Features";
import HowItWorks from "./components/HowItWorks";
import CTA from "./components/CTA";
import Footer from "./components/Footer";
import { Authcontext } from "./contexts/Authcontext";
import { useNavigate } from "react-router-dom";

function Root() {
  const auth = useContext(Authcontext);
  const navigate = useNavigate();
  useEffect(() => {
    if (auth.islogged) {
      navigate("/dashboard");
    }
  }, [auth]);
  return (
    <div className="min-h-screen bg-background ">
      <Navbar />
      <main>
        <Hero />
        <Features />
        <HowItWorks />
        <CTA />
      </main>
      <Footer />
    </div>
  );
}

export default Root;
