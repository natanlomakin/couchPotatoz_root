import React, { useEffect, useState } from "react";
import axios from "axios";
import { SERVER_URL } from "../utils/serverUtil";
import LinkButton from "../components/LinkButton";

const Groups = () => {
  const [groups, setGroups] = useState([]);
  const [groupIds, setGroupIds] = useState([]);
  const [users, setUsers] = useState("");

  useEffect(() => {
    const server_data = async () => {
      const response = await axios(SERVER_URL + "/groups/", {
        Accept: "application/json",
        "Content-Type": "application/json",
      });
      setGroups(response.data.data);
      setGroupIds(response.data.library_ids);
    };
    server_data();
  }, []);

  return (
    <div>
      <div className="mainContainer">
        <h1>Groups</h1>
        <div className="groups-view">
          {groups.map((group, ind) => (
            <div className="single-group" key={ind}>
              <h2>{group.title}</h2>
              <p>{group.summery}</p>
              {LinkButton("Visit", groupIds[ind])}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Groups;
