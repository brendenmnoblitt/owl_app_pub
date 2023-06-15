// Vue app instance
Vue.config.delimiters = ["${", "}"]; // Use "${" and "}" as delimiters
var app = new Vue({
  delimiters: ["${", "}"], // Use "${" and "}" as delimiters for this Vue instance
  el: "#app",
  data: {
    playerInfo: null,
    playerStats: null,
    joinedPlayers: [],
    teams: [],
  },
  mounted() {
    // Fetch player info and player stats data
    this.fetchPlayerInfo();
    this.fetchPlayerStats();
  },
  methods: {
    fetchPlayerInfo() {
      axios
        .get("/api/playerinfo")
        .then((response) => {
          this.playerInfo = response.data;
          this.mergePlayerData();
        })
        .catch((error) => {
          console.error("Error:", error);
        });
    },
    fetchPlayerStats() {
      axios
        .get("/api/playerstats")
        .then((response) => {
          //console.log(response.data)
          this.playerStats = response.data;
          this.mergePlayerData();
        })
        .catch((error) => {
          console.error("Error:", error);
        });
    },
    mergePlayerData() {
      // Check if both player info and player stats data are fetched
      if (this.playerInfo && this.playerStats) {
        // Perform the data merging based on the specified conditions
        // Join on currentTeam.teamId = id and playerInfo.name = player_name
        const joinedPlayers = this.playerInfo.map((info) => {
          const matchingStats = this.playerStats.find((stats) => {
            return (
              stats.id === info.currentTeam.teamId &&
              stats.player_name === info.playerInfo.name
            );
          });
          
          try { 
            info.playerInfo.role = info.playerInfo.role.toUpperCase()
          } catch { }
          
          return {
            playerId: info.playerId,
            playerMedia: info.playerMedia,
            currentTeam: info.currentTeam,
            playerInfo: info.playerInfo,
            playerStats: matchingStats,
          };
        });

        // Group joined players by team
        const teams = {};
        joinedPlayers.forEach((player) => {
          const teamId = player.currentTeam.teamId;
          if (!teams[teamId]) {
            teams[teamId] = {
              teamName: player.currentTeam.teamName,
              teamIcon: player.currentTeam.teamIcon,
              players: []
            };
          }
          teams[teamId].players.push(player);
        });

        // Convert teams object to array
        this.teams = Object.values(teams);
      }
    },
    getRoleIcon(role) {
      // Map the role to the corresponding CSS class
      if (role === 'OFFENSE') {
        return 'dps';
      } else if (role === 'TANK') {
        return 'tank';
      } else if (role === 'SUPPORT') {
        return 'support';
      } else {
        return '';
      }
    }
  },
});

Vue.filter('formatNumber', function(value) {
  try {
    return value.toLocaleString(undefined, { maximumFractionDigits: 0 });
  } catch { return 0 }
});
