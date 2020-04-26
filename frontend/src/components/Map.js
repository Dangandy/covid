// 3rd party exports
import React, { useMemo, memo } from "react";
import { scalePow } from "d3-scale";
import {
  ComposableMap,
  Geographies,
  Geography,
  Sphere,
  Graticule,
} from "react-simple-maps";
import styled from "styled-components";

// local imports
import formatNumber from "../utils/utils";

// variables
const geoUrl =
  "https://raw.githubusercontent.com/zcreativelabs/react-simple-maps/master/topojson-maps/world-110m.json";

const ToolTip = styled.div`
  display: flex;
  flex-direction: column;
  line-height: 1.25rem;
  span {
    font-size: 1rem;
  }
`;

const Title = styled.span`
  font-size: 1.25rem;
  font-weight: 600;
`;

const Tip = styled.small`
  margin: 0;
`;

const isoMap = {
  Afghanistan: "AFG",
  Albania: "ALB",
  Algeria: "DZA",
  Andorra: "AND",
  Angola: "AGO",
  "Antigua and Barbuda": "ATG",
  Argentina: "ARG",
  Armenia: "ARM",
  Australia: "AUS",
  Austria: "AUT",
  Azerbaijan: "AZE",
  Bahamas: "BHS",
  Bahrain: "BHR",
  Bangladesh: "BGD",
  Barbados: "BRB",
  Belarus: "BLR",
  Belgium: "BEL",
  Belize: "BLZ",
  Benin: "BEN",
  Bhutan: "BTN",
  Bolivia: "BOL",
  "Bosnia and Herzegovina": "BIH",
  Botswana: "BWA",
  Brazil: "BRA",
  Brunei: "BRN",
  Bulgaria: "BGR",
  "Burkina Faso": "BFA",
  Burma: "MMR",
  Burundi: "BDI",
  "Cabo Verde": null,
  Cambodia: "KHM",
  Cameroon: "CMR",
  Canada: "CAN",
  "Central African Republic": "CAF",
  Chad: "TCD",
  Chile: "CHL",
  China: "CHN",
  Colombia: "COL",
  "Congo (Brazzaville)": "COG",
  "Congo (Kinshasa)": "COD",
  "Costa Rica": "CRI",
  "Cote d'Ivoire": "CIV",
  Croatia: "HRV",
  Cuba: "CUB",
  Cyprus: "CYP",
  Czechia: "CZE",
  Denmark: "DNK",
  "Diamond Princess": null,
  Djibouti: "DJI",
  Dominica: "DMA",
  "Dominican Republic": "DOM",
  Ecuador: "ECU",
  Egypt: "EGY",
  "El Salvador": "SLV",
  "Equatorial Guinea": "GNQ",
  Eritrea: "ERI",
  Estonia: "EST",
  Eswatini: "SWZ",
  Ethiopia: "ETH",
  Fiji: "FJI",
  Finland: "FIN",
  France: "FRA",
  Gabon: "GAB",
  Gambia: "GMB",
  Georgia: "GEO",
  Germany: "DEU",
  Ghana: "GHA",
  Greece: "GRC",
  Grenada: "GRD",
  Guatemala: "GTM",
  Guinea: "GIN",
  "Guinea-Bissau": "GNB",
  Guyana: "GUY",
  Haiti: "HTI",
  "Holy See": null,
  Honduras: "HND",
  Hungary: "HUN",
  Iceland: "ISL",
  India: "IND",
  Indonesia: "IDN",
  Iran: "IRN",
  Iraq: "IRQ",
  Ireland: "IRL",
  Israel: "ISR",
  Italy: "ITA",
  Jamaica: "JAM",
  Japan: "JPN",
  Jordan: "JOR",
  Kazakhstan: "KAZ",
  Kenya: "KEN",
  "Korea, South": "KOR",
  Kosovo: "XKX",
  Kuwait: "KWT",
  Kyrgyzstan: "KGZ",
  Laos: "LAO",
  Latvia: "LVA",
  Lebanon: "LBN",
  Liberia: "LBR",
  Libya: "LBY",
  Liechtenstein: "LIE",
  Lithuania: "LTU",
  Luxembourg: "LUX",
  "MS Zaandam": null,
  Madagascar: "MDG",
  Malawi: "MWI",
  Malaysia: "MYS",
  Maldives: "MDV",
  Mali: "MLI",
  Malta: "MLT",
  Mauritania: "MRT",
  Mauritius: "MUS",
  Mexico: "MEX",
  Moldova: "MDA",
  Monaco: "MCO",
  Mongolia: "MNG",
  Montenegro: "MNE",
  Morocco: "MAR",
  Mozambique: "MOZ",
  Namibia: "NAM",
  Nepal: "NPL",
  Netherlands: "NLD",
  "New Zealand": "NZL",
  Nicaragua: "NIC",
  Niger: "NER",
  Nigeria: "NGA",
  "North Macedonia": "MKD",
  Norway: "NOR",
  Oman: "OMN",
  Pakistan: "PAK",
  Panama: "PAN",
  "Papua New Guinea": "PNG",
  Paraguay: "PRY",
  Peru: "PER",
  Philippines: "PHL",
  Poland: "POL",
  Portugal: "PRT",
  Qatar: "QAT",
  Romania: "ROU",
  Russia: "RUS",
  Rwanda: "RWA",
  "Saint Kitts and Nevis": "KNA",
  "Saint Lucia": "LCA",
  "Saint Vincent and the Grenadines": "VCT",
  "San Marino": "SMR",
  "Sao Tome and Principe": "STP",
  "Saudi Arabia": "SAU",
  Senegal: "SEN",
  Serbia: "SRB",
  Seychelles: "SYC",
  "Sierra Leone": "SLE",
  Singapore: "SGP",
  Slovakia: "SVK",
  Slovenia: "SVN",
  Somalia: "SOM",
  "South Africa": "ZAF",
  "South Sudan": "SSD",
  Spain: "ESP",
  "Sri Lanka": "LKA",
  Sudan: "SDN",
  Suriname: "SUR",
  Sweden: "SWE",
  Switzerland: "CHE",
  Syria: "SYR",
  "Taiwan*": "TWN",
  Tanzania: "TZA",
  Thailand: "THA",
  "Timor-Leste": "TLS",
  Togo: "TGO",
  "Trinidad and Tobago": "TTO",
  Tunisia: "TUN",
  Turkey: "TUR",
  US: "USA",
  Uganda: "UGA",
  Ukraine: "UKR",
  "United Arab Emirates": "ARE",
  "United Kingdom": "GBR",
  Uruguay: "URY",
  Uzbekistan: "UZB",
  Venezuela: "VEN",
  Vietnam: "VNM",
  "West Bank and Gaza": "PSE",
  "Western Sahara": "ESH",
  Yemen: "YEM",
  Zambia: "ZMB",
  Zimbabwe: "ZWE",
};

const MapChart = ({ max, setTooltipContent, data }) => {
  const colorScale = useMemo(() => {
    return scalePow()
      .exponent(0.5)
      .domain([0, max])
      .range(["#e6acac", "#e60505"]);
  }, [max]);

  return (
    <>
      <ComposableMap
        data-tip=""
        height={400}
        projectionConfig={{
          scale: 150,
        }}
      >
        <Sphere stroke="#E4E5E6" strokeWidth={0.5} />
        <Graticule stroke="#E4E5E6" strokeWidth={0.5} />
        <Geographies geography={geoUrl}>
          {({ geographies }) =>
            geographies.map((geo) => {
              const d = data.find((s) => {
                const iso = isoMap[s.country];
                return iso === geo.properties.ISO_A3;
              });
              return (
                <Geography
                  key={geo.rsmKey}
                  geography={geo}
                  fill={d ? colorScale(d.confirmed) : "#E6d1d1"}
                  onMouseEnter={() => {
                    if (d) {
                      setTooltipContent(
                        <ToolTip>
                          <Title>{d.country}</Title>
                          <span>Confirmed: {formatNumber(d.confirmed)}</span>
                          <span>Recovered: {formatNumber(d.recovered)}</span>
                          <span>Deaths: {formatNumber(d.deaths)}</span>
                          {d.confirmed_pred ? (
                            <span>
                              Predicted Cases: {formatNumber(d.confirmed_pred)}
                            </span>
                          ) : (
                            ""
                          )}
                        </ToolTip>
                      );
                    }
                  }}
                  onMouseLeave={() => {
                    setTooltipContent("");
                  }}
                  style={{
                    hover: {
                      stroke: "dimgray",
                      strokeWidth: 0.7,
                      outline: "none",
                    },
                    pressed: {
                      stroke: "dimgray",
                      strokeWidth: 1,
                      outline: "none",
                    },
                  }}
                />
              );
            })
          }
        </Geographies>
      </ComposableMap>
      <Tip>Hover for details</Tip>
    </>
  );
};

export default memo(MapChart);
