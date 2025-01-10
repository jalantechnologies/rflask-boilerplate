import { useCallback, useState } from 'react';

import { UseAsyncResponse, AsyncResult, AsyncError } from '../types';
import { AsyncOperationError } from '../types/async-operation';
import { Nullable } from '../types/common-types';

const useAsync = <T>(
  asyncFn: (...args: unknown[]) => Promise<AsyncResult<T>>,
): UseAsyncResponse<T> => {
  const [result, setResult] = useState<Nullable<T>>(null);
  const [isLoading, setLoading] = useState(false);
  const [error, setError] = useState<Nullable<AsyncError>>(null);

  const asyncCallback = useCallback(
    async (...args: unknown[]) => {
      setError(null);
      setLoading(true);
      try {
        const response = await asyncFn(...args);

        if (response.data !== undefined) {
          setResult(response.data);
        }

        return response.data ?? null;
      } catch (e) {
        const err = new AsyncOperationError({
          code: e?.response?.data?.code || e.code,
          message: e?.response?.data?.message || e.message,
        });

        setError(err);
        throw new Error(err.message);
      } finally {
        setLoading(false);
      }
    },
    [asyncFn],
  );
  return {
    asyncCallback,
    error,
    isLoading,
    result,
  };
};
export default useAsync;
