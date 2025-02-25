import { createContext, useContext } from 'react';

const AuthContext = createContext();

const AuthContextProvider = ({children}) => {


    return (
        <AuthContext.Provider value={{}} >
            {children}
        </AuthContext.Provider>
    )
}

const useAuthContext = useContext(AuthContext);

export default useAuthContext;