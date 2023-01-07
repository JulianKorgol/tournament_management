import React, { useRef } from "react";
import styles from "./AddPeopleToTournament.module.scss";
import { get, post } from "../../functions/Requests/Requests";
import AppContext from "../../functions/AppContext/AppContext";


const AddPeopleToTournament = (props) => {
    const [people, setPeople] = React.useState([]);
    const { uuid } = props;
    const { MakeToast } = React.useContext(AppContext);

    const getPeople = async () => {
        const response = await get(`coordinator_panel/tournament/${uuid}/manage/user/add/`, { withCredentials: true }).catch(err => err.response);
        if (response.status === 200) {
            setPeople(response.data.accounts);
        }
    }

    React.useEffect(() => {
        getPeople();
    }, []);

    const addPeople = async (e) => {
        e.preventDefault();

        const addPeople_username = e.target.person.value;
        const addPeople_role = e.target.role.value;

        const response = await post(`coordinator_panel/tournament/${uuid}/manage/user/add/`, {username: addPeople_username, role: addPeople_role}, { withCredentials: true }).catch(err => err.response);
        if (response.status === 200) {
            MakeToast("Dodano użytkownika", "success");
        } else {
            if (response.data.error === "User already in tournament") {
                MakeToast("Użytkownik należy już do tego turnieju.", "error");
            } else {
                MakeToast("Coś poszło nie tak...", "error");
            }
        }
    }

    return (
        <div className={styles.wrapper}>
            <h4>Dodaj uczestników do turnieju</h4>
            <form onSubmit={addPeople}>
                <div className={styles.selects}>
                    <div className={styles.select}>
                        <p>Rola:</p>
                        <select name="role">
                            <option value="player">Gracz</option>
                            <option value="coordinator">Kordynator</option>
                        </select>
                    </div>
                    <div className={styles.select}>
                        <p>Osoba:</p>
                        <select name="person">
                            {people.map(person => {
                                return <option key={person.username} value={person.username}>{person.first_name} {person.last_name}</option>
                            })}
                        </select>
                    </div>
                </div>
                <div className={styles.submit}>
                    <input type="submit" value="Dodaj" />
                </div>
            </form>
        </div>
    );
}

export default AddPeopleToTournament;