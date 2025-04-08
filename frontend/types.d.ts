declare module '@apollo/client' {
  export interface ApolloClientOptions<TCacheShape> {
    link: any;
    cache: any;
    defaultOptions?: any;
  }

  export class ApolloClient<TCacheShape> {
    constructor(options: ApolloClientOptions<TCacheShape>);
  }

  export function createHttpLink(options: any): any;
  export class InMemoryCache {
    constructor(options?: any);
  }

  export function gql(literals: any, ...placeholders: any[]): any;
  export function useQuery(query: any, options?: any): {
    loading: boolean;
    error?: any;
    data?: any;
    refetch: () => Promise<any>;
  };

  export function useMutation(mutation: any, options?: any): [
    (options?: any) => Promise<any>,
    {
      loading: boolean;
      error?: any;
      data?: any;
    }
  ];

  export const ApolloProvider: React.FC<{client: ApolloClient<any>}>;
}

// Declare module resolution for .ts files to help with TypeScript errors
declare module '*.ts' {
  const content: any;
  export default content;
  export * from content;
} 