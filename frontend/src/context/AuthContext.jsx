import React, { createContext, useContext, useState} from "react";
import Cookies from 'js-cookie';

const AuthContext = createContext();

const AuthContextProvider = ({children}) => {

    const [ token, setToken ] = useState(Cookies.get('token') || "");
    const [ email, setEmail ] = useState(Cookies.get('email') || "");
    const [ name, setName ] = useState(Cookies.get('name') || "");

    const isLoggedIn = !!token;

    return(
        <AuthContext.Provider value={{
            isLoggedIn,
            token, setToken,
            email, setEmail,
            name, setName,
        }}>
        {children}
      </AuthContext.Provider>
    )
}; 


const useAuthContext = () => useContext(AuthContext);

export default useAuthContext;
export { AuthContextProvider };