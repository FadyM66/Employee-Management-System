import React from 'react';
import fetcher from './fetcher';
import { sessionDataHandler } from './handlers.js';

export const handleLoginSubmit = async (values, { setSubmitting, setFieldError }, setSubmissionResult) => {

    setSubmitting(true);
    try {
        let returns = {
            "token": true,
            "email": true,
            "name": "Fady"
        }
        sessionDataHandler(returns)
        setSubmissionResult(returns)
    }
    catch (error) {
        console.log("failed: ", error)
    }
}