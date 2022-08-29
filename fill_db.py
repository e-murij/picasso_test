from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine, DateTime, Time, Integer


def log(func):
    def wrapper(*args, **kwargs):
        startTime = datetime.now()
        result = func(*args, **kwargs)
        with open("log.txt", "a", encoding="UTF-8") as file:
            file.write(f"Used time:{datetime.now() - startTime}, processed incidents: {result}\n")
        return result

    return wrapper


@log
def from_csv_to_sql(file):
    df = pd.read_csv(file)
    df = df.fillna('not defined')
    try:
        engine = create_engine('postgresql://postgres:admin@localhost:5432/postgres')
        df.to_sql(name='pandas_police_department_calls_for_service_dump',
                  con=engine,
                  if_exists='replace',
                  dtype={"Report Date": DateTime(), "Call Date": DateTime(), "Offense Date": DateTime(),
                         "Call Date Time": DateTime(), "Call Time": Time(), "Agency Id": Integer()}
                  )
        with engine.begin() as conn:
            conn.execute(
                """INSERT INTO city (name)
                   SELECT DISTINCT pd."City"
                   FROM pandas_police_department_calls_for_service_dump pd
                   ON CONFLICT (name) DO NOTHING"""
            )
            conn.execute(
                """INSERT INTO original_crime_type_name (name)
                   SELECT DISTINCT pd."Original Crime Type Name"
                   FROM pandas_police_department_calls_for_service_dump pd
                   ON CONFLICT (name) DO NOTHING"""
            )
            conn.execute(
                """INSERT INTO disposition (name)
                   SELECT DISTINCT pd."Disposition"
                   FROM pandas_police_department_calls_for_service_dump pd
                   ON CONFLICT (name) DO NOTHING"""
            )
            conn.execute(
                """INSERT INTO state (name)
                   SELECT DISTINCT pd."State"
                   FROM pandas_police_department_calls_for_service_dump pd
                   ON CONFLICT (name) DO NOTHING"""
            )
            conn.execute(
                """INSERT INTO agency_id (name)
                   SELECT DISTINCT pd."Agency Id"
                   FROM pandas_police_department_calls_for_service_dump pd
                   ON CONFLICT (name) DO NOTHING"""
            )
            conn.execute(
                """INSERT INTO address_type (name)
                   SELECT DISTINCT pd."Address Type"
                   FROM pandas_police_department_calls_for_service_dump pd
                   ON CONFLICT (name) DO NOTHING"""
            )
            result = conn.execute(
                """ INSERT INTO police_department_calls_for_service (
                        crime_id, original_crime_type_name_id, report_date, call_date, offense_date, call_time, call_date_time,
                        disposition_id, address, city_id, state_id, agency_id, address_type_id, common_location)
                    SELECT
                        pd."Crime Id", original_crime_type_name.id, pd."Report Date", pd."Call Date", pd."Offense Date",
                        pd."Call Time", pd."Call Date Time", disposition.id, pd."Address", city.id, state.id, agency_id.id,
                        address_type.id, pd."Common Location"
                     FROM pandas_police_department_calls_for_service_dump pd
                     JOIN original_crime_type_name
                           ON original_crime_type_name.name = pd."Original Crime Type Name"
                     JOIN disposition
                           ON disposition.name = pd."Disposition"
                     JOIN city
                           ON city.name = pd."City"
                     JOIN state
                           ON state.name = pd."State"
                     JOIN agency_id
                           ON agency_id.name = pd."Agency Id"
                     JOIN address_type
                           ON address_type.name = pd."Address Type" """
            )
            result = result.rowcount
            conn.execute("DROP TABLE pandas_police_department_calls_for_service_dump")
            return result
    except Exception as error:
        print(error)


if __name__ == "__main__":
    from_csv_to_sql('police-department-calls-for-service.csv')
