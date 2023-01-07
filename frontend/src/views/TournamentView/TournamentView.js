import React from "react";
import styles from "./TournamentView.module.scss";
import { get, post } from "../../functions/Requests/Requests";
import AppContext from "../../functions/AppContext/AppContext";
import {redirect, useNavigate} from "react-router";
import User from "../../functions/UserContext/UserContext";
import { useParams } from "react-router-dom";
import Matches from "../../components/Matches/Matches";
import AddPeopleToTournament from "../../components/AddPeopleToTournament/AddPeopleToTournament";
import AddResultsToTournaments from "../../components/AddResultsToTournaments/AddResultsToTournaments";


const TournamentView = () => {
    const [tournament, setTournament] = React.useState({});
    const { setLoading, MakeToast, refreshPage } = React.useContext(AppContext);
    const { checkLogin } = React.useContext(User);
    const [message, setMessage] = React.useState("");
    const [status, setStatus] = React.useState("success");
    const { user } = React.useContext(User);
    const redirection = useNavigate();
    let { uuid } = useParams();

    const [buttonAddPeopleopen, setButtonAddPeopleopen] = React.useState(false);
    const [buttonAddResultsopen, setButtonAddResultsopen] = React.useState(false);

    const checkUser = async () => {
        const logged = await checkLogin();
        if (!logged) {
            redirection("/login");
        }
    }

    const tournamentData = async () => {
        setLoading(true);

        const response = await get(`dashboard/tournament/${uuid}/`, { withCredentials: true }).catch(err => err.response);
        if (response.status === 200) {
            setTournament(response.data.tournament);
        }

        setLoading(false);
    }

    React.useEffect(() => {
        checkUser();
        tournamentData();
    }, []);

    const GenerateMatches = async () => {
        setLoading(true);

        const response = await get(`coordinator_panel/tournament/${uuid}/manage/games/generate/`, { withCredentials: true }).catch(err => err.response);
        if (response.status === 200) {
            MakeToast("Pomyślnie wygenerowano mecze", "success");
        }

        setLoading(false);
        refreshPage();
    }


    return (
        <div className={styles.wrapper}>
            <h1>Turniej: {tournament.name}</h1>
            <div className={styles.content}>
                <h4>Informacje o turnieju</h4>
                <p>Opis: {tournament.description}</p>
                {user["role"] === "admin" || user["role"] === "coordinator" ?
                <p className={styles.vip}>Twoje uprawnienia pozwalają na zarządzanie tym turniejem.</p> : null}
            </div>
            {user["role"] === "admin" || user["role"] === "coordinator" ?
                <div className={styles.manage}>
                    <button className={styles.button_add} onClick={() => {setButtonAddResultsopen(!buttonAddResultsopen)}}>Dodaj wynik</button>
                    <button className={styles.button_modify}>Zmodyfikuj wynik</button>
                    <button className={styles.button_modify} onClick={() => {setButtonAddPeopleopen(!buttonAddPeopleopen)}}>Dodaj osoby</button>
                    <button className={styles.button_modify} onClick={GenerateMatches}>Stwórz mecze, każdy z każdym</button>
                    <button className={styles.button_delete}>Usuń wynik</button>
                    <button className={styles.button_show}>Wyświetl nierozegrane mecze</button>
                </div>
            : null}
            <div>
                {buttonAddPeopleopen ? <div><AddPeopleToTournament uuid={uuid}/></div> : null}
                {buttonAddResultsopen ? <div><AddResultsToTournaments uuid={uuid}/></div> : null}
            </div>
            <div className={styles.matches}>
                <h4>Aktualne wyniki</h4>
                <div className={styles.matches_list}>
                    <Matches tournament={uuid} />
                </div>
            </div>
        </div>
    );
}

export default TournamentView;