interface Props {
  data: Record<string, string | number>[];
}

export function DataTable({ data }: Props) {
  if (!data.length) return null;
  const columns = Object.keys(data[0]);

  return (
    <div className="overflow-x-auto rounded-lg border border-border/50">
      <table className="w-full text-sm">
        <thead>
          <tr className="bg-muted/60">
            {columns.map((col) => (
              <th key={col} className="px-3 py-2 text-left font-semibold text-foreground whitespace-nowrap">
                {col}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.map((row, i) => (
            <tr key={i} className="border-t border-border/30 hover:bg-muted/30 transition-colors">
              {columns.map((col) => (
                <td key={col} className="px-3 py-2 text-secondary-foreground whitespace-nowrap">
                  {row[col]}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
