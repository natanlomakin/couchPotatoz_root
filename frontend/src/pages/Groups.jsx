import React, { useEffect, useState } from "react";
import axios from "axios";
import { SERVER_URL } from "../utils/serverUtil";
import LinkButton from "../components/LinkButton";

const Groups = () => {
  const [groups, setGroups] = useState([]);
  const [groupIds, setGroupIds] = useState([]);
  const [users, setUsers] = useState("");
  const [groupSearchValue, setGroupSearchValue] = useState("");

  useEffect(() => {
    const server_data = async () => {
      const response = groupSearchValue
        ? await axios(SERVER_URL + "/groups/search/" + groupSearchValue, {
            headers: {
              Accept: "application/json",
              "Content-Type": "application/json",
            },
          })
        : await axios(SERVER_URL + "/groups/", {
            headers: {
              Accept: "application/json",
              "Content-Type": "application/json",
            },
          });
      setGroups(response.data.data);
      setGroupIds(response.data.groups_ids);
      console.log(response.data.data);
    };
    server_data();
  }, [groupSearchValue]);

  return (
    <div>
      <div className="mainContainer">
        <div className="group-search">
          <h3>
            Search:{" "}
            <input
              type="text"
              placeholder="Group title"
              autoComplete={"false"}
              onChange={(e) => {
                setGroupSearchValue(e.target.value);
              }}
            ></input>
          </h3>
        </div>
        <h1>Groups</h1>
        <div className="groups-view">
          {groups ? (
            groups.map((group, ind) => (
              <div className="single-group" key={ind}>
                {console.log(group[ind])}
                <h2>{group.title}</h2>
                <p>{group.summery}</p>
                {LinkButton("Visit", groupIds[ind])}
              </div>
            ))
          ) : (
            <div>
              <h2>No groups were found</h2>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Groups;
