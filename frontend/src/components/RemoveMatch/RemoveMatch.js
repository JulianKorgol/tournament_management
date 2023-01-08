import React from "react";
import styles from './RemoveMatch.module.scss';
import AppContext from "../../functions/AppContext/AppContext";
import { get, post } from "../../functions/Requests/Requests";


const RemoveMatch = (props) => {
    const [games, setGames] = React.useState([]);
    const { MakeToast, refreshPage } = React.useContext(AppContext);
    const { uuid } = props

    const getMatches = async () => {
        const response = await get(`coordinator_panel/tournament/${uuid}/score/delete/`, {withCredentials: true}).catch(err => err.response);

        if (response.status === 200) {
            setGames(response.data.games);
        }
    }

    const deleteMatch = async (e) => {
        e.preventDefault();
        const match = e.target.match.value;

        const response = await post(`coordinator_panel/tournament/${uuid}/score/delete/`, { game_id: match }, {withCredentials: true}).catch(err => err.response);

        if (response.status === 200) {
            if (response.data.success === true) {
                MakeToast("Pomyślnie usunięto mecz", "success");
                refreshPage();
                return;
            }
            MakeToast("Nie udało się usunąć meczu", "error");
        }
    }

    React.useEffect(() => {
        getMatches();
    }, []);

    return (
        <div className={styles.wrapper}>
            <h4>Usuń wynik</h4>
            <form onSubmit={deleteMatch}>
                    <div className={styles.select}>
                        <p>Wynik:</p>
                        <select name="match">
                            {games.map((game) => {
                                if (game.player1_score !== null && game.player2_score !== null) {
                                return <option key={game.id}
                                    value={game.id}>{game.player1} - {game.player2} ({game.player1_score}:{game.player2_score})</option>
                                }
                            })}
                        </select>
                    </div>
                <div className={styles.submit}>
                    <input type="submit" value="Usuń" />
                </div>
            </form>
        </div>
    )
}

export default RemoveMatch;