import React from "react";
import { Button } from "@/components/ui/button";
import { motion } from "framer-motion";
import { LampContainer } from "./ui/lamp";
function CTA() {
  return (
    <div className="flex flex-col items-center ">
      <LampContainer className="">
        <motion.h1
          initial={{ opacity: 0.5, y: 100 }}
          whileInView={{ opacity: 1, y: 30 }}
          transition={{
            delay: 0.3,
            duration: 0.8,
            ease: "easeInOut",
          }}
          className="mt-8 bg-gradient-to-br from-slate-300 to-slate-500 py-4  bg-clip-text text-center text-4xl font-medium tracking-tight text-transparent justify-center md:text-7xl"
        >
          Ready to dive in?
          <br /> Start your RAG project today
          <br />
          <br />
          <span className="hover:cursor-pointer hover:bg-gray-800/40 hover:text-white max-w-2xl rounded-full mx-auto text-center px-10 ">
            Get started
          </span>
        </motion.h1>
      </LampContainer>
    </div>
  );
}

export default CTA;
