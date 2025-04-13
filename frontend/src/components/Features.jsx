import React from "react";
import {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
} from "@/components/ui/card";
import { Database, Search, Zap } from "lucide-react";

function Features() {
  const features = [
    {
      name: "Enhanced Knowledge Retrieval",
      description:
        "Access vast amounts of external data to supplement AI responses.",
      icon: Database,
    },
    {
      name: "Improved Accuracy",
      description:
        "Leverage up-to-date information for more precise and relevant outputs.",
      icon: Search,
    },
    {
      name: "Real-time Augmentation",
      description:
        "Dynamically incorporate retrieved information into AI-generated content.",
      icon: Zap,
    },
  ];

  return (
    <section id="features" className="py-12 bg-gray-50 dark:bg-gray-900  z-10">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="lg:text-center">
          <h2 className="text-base text-primary font-semibold tracking-wide uppercase ">
            Features
          </h2>
          <p className="mt-2 text-3xl leading-8 font-extrabold tracking-tight text-gray-900 sm:text-4xl dark:text-neutral-300">
            Powerful RAG Capabilities
          </p>
          <p className="mt-4 max-w-2xl text-xl text-gray-500 dark:text-neutral-400 lg:mx-auto">
            Discover how our RAG project can revolutionize your AI applications.
          </p>
        </div>

        <div className="mt-10">
          <div className="grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-3">
            {features.map((feature) => (
              <Card key={feature.name} className="hover:opacity-80 hover:ring-[8px] dark:hover:ring-gray-800/60 transition-all duration-500 bg-white dark:bg-gray-800 ring-gray-300/60"  >
                <CardHeader>
                  <div className="flex items-center space-x-4" >

                  <feature.icon
                    className="h-6 w-6 text-primary"
                    aria-hidden="true"
                  />
                  <CardTitle>{feature.name}</CardTitle>
                  </div>
                  <CardDescription className="text-left">{feature.description}</CardDescription>
                </CardHeader>
              </Card>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}

export default Features;
