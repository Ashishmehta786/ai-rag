import { createContext, useEffect, useState } from "react";
import { auth } from "../hooks/Firebase";

const Authcontext = createContext(null);

const Authprovider = ({ children }) => {
  const [user, setuser] = useState({});
  const [islogged, setislogged] = useState(false);
  useEffect(() => {
    const unsubscribe = async () => {
      const resp = auth.onAuthStateChanged((user) => {
        if (user) {
          setislogged(true);
          setuser(user);
        } else {
          setuser(null);
        }
      });
    };
    return () => unsubscribe();
  }, [user]);

  return (
    <Authcontext.Provider
      value={{
        user,
        setuser,
        islogged,
        setislogged,
      }}
    >
      {children}
    </Authcontext.Provider>
  );
};

export { Authcontext, Authprovider };
