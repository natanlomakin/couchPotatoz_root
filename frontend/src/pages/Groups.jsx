import React from "react";
import Header from "../components/Header";
import axios from "axios";

const Groups = () => {
  const [groups, setGroups] = useState("");

  useEffect(() => {
    const server_data = async () => {};
  }, []);

  return (
    <div>
      <Header />
      <div className="mainContainer">
        <h1>Groups</h1>
      </div>
    </div>
  );
};

export default Groups;
