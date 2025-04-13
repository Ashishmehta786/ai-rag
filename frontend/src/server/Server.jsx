import argon2 from "argon2";
async function SavePassword(password) {
  const hashpassword = await argon2.hash(password);
  
}
