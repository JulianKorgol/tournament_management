import React from "react";
import styles from './AddResultsToTournaments.module.scss';
import { get, post } from '../../functions/Requests/Requests';
import AppContext from "../../functions/AppContext/AppContext";


const AddResultsToTournaments = (props) => {
    const { uuid } = props;
    const [people, setPeople] = React.useState([]);
    const { MakeToast } = React.useContext(AppContext);

    const takeResults = async () => {
        const response = await get(`coordinator_panel/tournament/${uuid}/score/add/`, { withCredentials: true }).catch(err => err.response);
        if (response.status === 200) {
            setPeople(response.data.players);
        }
    }

    const addResult = async (e) => {
        e.preventDefault();

        const player1 = e.target.person1.value;
        const player2 = e.target.person2.value;
        const score1 = e.target.score1.value;
        const score2 = e.target.score2.value;

        const response = await post(`coordinator_panel/tournament/${uuid}/score/add/`, { player1: player1, player2: player2, player1_score: score1, player2_score: score2 }, { withCredentials: true }).catch(err => err.response);
        if (response.status === 200) {
            MakeToast("Pomyślnie dodano wyniki", "success");
            e.target.reset();
        } else if (response.status === 400) {
            if (response.data.error === "Invalid data") {
                MakeToast("Wprowadzone dane są niepoprawne.", "error");
            } else {
                MakeToast("Coś poszło nie tak...", "error");
            }
        }
    }

    React.useEffect(() => {
        takeResults();
    }, []);

    return (
        <div className={styles.wrapper}>
            <h4>Dodaj wynik</h4>
            <form onSubmit={addResult}>
                <div className={styles.form}>
                    <div className={styles.data}>
                        <p>Gracz 1:</p>
                        <select name="person1">
                            {people.map(person => {
                                return <option key={person.username} value={person.username}>{person.first_name} {person.last_name}</option>
                            })}
                        </select>
                    </div>
                    <div className={styles.data}>
                        <p>Gracz 2:</p>
                        <select name="person2">
                            {people.map(person => {
                                return <option key={person.username} value={person.username}>{person.first_name} {person.last_name}</option>
                            })}
                        </select>
                    </div>
                    <div className={styles.data}>
                        <p>Wynik gracz 1:</p>
                        <input type="number" name="score1" />
                    </div>
                    <div className={styles.data}>
                        <p>Wynik gracz 2:</p>
                        <input type="number" name="score2" />
                    </div>
                </div>
                <div className={styles.submit}>
                    <input type="submit" value="Dodaj" />
                </div>
            </form>
        </div>
    );
}

export default AddResultsToTournaments;