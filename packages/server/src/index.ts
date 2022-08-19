import 'reflect-metadata';
import { ApolloServer } from 'apollo-server-express';
import { ApolloServerPluginDrainHttpServer, ApolloServerPluginLandingPageLocalDefault } from 'apollo-server-core';
import express from 'express';
import * as http from 'http';
import schema from './resolver';
import { PostgresDataSource } from './data-source';

async function startApolloServer(schema) {
    await PostgresDataSource.initialize();

    const app = express();
    const httpServer = http.createServer(app);
    const server = new ApolloServer({
        schema,
        csrfPrevention: true,
        cache: 'bounded',
        plugins: [
            ApolloServerPluginDrainHttpServer({ httpServer }),
            ApolloServerPluginLandingPageLocalDefault({ embed: true }),
        ],
        // dataSources: () => ({ db:  }),
    });

    await server.start();
    server.applyMiddleware({
        app,
        path: '/',
    });

    await new Promise<void>((resolve) => httpServer.listen({ port: 4000 }, resolve));
    console.log(`🚀 Server ready at http://localhost:4000${server.graphqlPath}`);
}

startApolloServer(schema);
