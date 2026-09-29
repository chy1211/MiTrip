import React, { createContext, useContext, useState, useEffect } from 'react';
import { API_BASE_URL } from '../constants/config';

const CityDataContext = createContext();


export const CityDataProvider = ({ children }) => {
    const [cityData, setCityData] = useState([]);
    useEffect(() => {

        const fetchData = async () => {
            try {
                const response = await fetch(`${API_BASE_URL}/api/explore/checkHottestCity`);
                const json = await response.json();
                setCityData(json);

            } catch (error) {
                console.error(error);

            }
        };
        fetchData();

        
    }, []);
    console.log('CityDataContext:',cityData);
    return (
        <CityDataContext.Provider value={cityData}>
            {children}
        </CityDataContext.Provider>
    );
};

export const useCityData = () => {
    return useContext(CityDataContext);
};