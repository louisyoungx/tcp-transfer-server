from Server.api import serverLog, serverConfig, signIn, stop

URL_TABLE = {
    "/log": serverLog,
    "/config": serverConfig,
    "/sign-in": signIn,
    "/stop": stop,
}
