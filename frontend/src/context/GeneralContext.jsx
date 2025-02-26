import React, { createContext, useContext, useState} from "react";
import { useNavigate } from 'react-router-dom';

const GeneralContext = createContext();

const GeneralContextProvider = ({children}) => {

    const navigate = useNavigate();

    return(
        <GeneralContext.Provider value={{
            navigate
        }}>
            {children}
        </GeneralContext.Provider>
    )
}; 


const useGeneralContext = useContext(GeneralContext);

export default useGeneralContext;