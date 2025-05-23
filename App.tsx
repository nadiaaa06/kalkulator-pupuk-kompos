import React, { useState } from 'react';
import { 
  Container, 
  Paper, 
  Typography, 
  TextField, 
  Button, 
  Box,
  Grid,
  Divider,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow
} from '@mui/material';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import { calculateCompoundOxidation, parseCompound } from './utils/periodicTable';

const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
  },
});

interface ReactionInput {
  reactants: string;
  products: string;
}

interface OxidationResult {
  compound: string;
  elements: { element: string; count: number; oxidation: number }[];
}

function App() {
  const [reaction, setReaction] = useState<ReactionInput>({
    reactants: '',
    products: ''
  });
  const [results, setResults] = useState<{
    reactants: OxidationResult[];
    products: OxidationResult[];
  } | null>(null);

  const handleInputChange = (field: keyof ReactionInput) => (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    setReaction({
      ...reaction,
      [field]: event.target.value
    });
  };

  const calculateRedox = () => {
    const reactants = reaction.reactants.split('+').map(r => r.trim());
    const products = reaction.products.split('+').map(p => p.trim());

    const reactantResults: OxidationResult[] = reactants.map(compound => {
      const elements = parseCompound(compound);
      const oxidationNumbers = calculateCompoundOxidation(compound);
      
      return {
        compound,
        elements: elements.map(({ element, count }) => ({
          element,
          count,
          oxidation: oxidationNumbers[element]
        }))
      };
    });

    const productResults: OxidationResult[] = products.map(compound => {
      const elements = parseCompound(compound);
      const oxidationNumbers = calculateCompoundOxidation(compound);
      
      return {
        compound,
        elements: elements.map(({ element, count }) => ({
          element,
          count,
          oxidation: oxidationNumbers[element]
        }))
      };
    });

    setResults({
      reactants: reactantResults,
      products: productResults
    });
  };

  return (
    <ThemeProvider theme={theme}>
      <Container maxWidth="md">
        <Box sx={{ my: 4 }}>
          <Typography variant="h3" component="h1" gutterBottom align="center">
            Redox Reaction Calculator
          </Typography>
          
          <Paper elevation={3} sx={{ p: 3, mb: 3 }}>
            <Grid container spacing={3}>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  label="Reactants (separate with +)"
                  value={reaction.reactants}
                  onChange={handleInputChange('reactants')}
                  placeholder="e.g., Fe + O2"
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  label="Products (separate with +)"
                  value={reaction.products}
                  onChange={handleInputChange('products')}
                  placeholder="e.g., Fe2O3"
                />
              </Grid>
              <Grid item xs={12}>
                <Button 
                  variant="contained" 
                  color="primary" 
                  fullWidth 
                  onClick={calculateRedox}
                >
                  Calculate Redox
                </Button>
              </Grid>
            </Grid>
          </Paper>

          {results && (
            <Paper elevation={3} sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom>
                Oxidation Numbers:
              </Typography>
              <Divider sx={{ my: 2 }} />
              
              <Typography variant="subtitle1" gutterBottom>
                Reactants:
              </Typography>
              <TableContainer>
                <Table size="small">
                  <TableHead>
                    <TableRow>
                      <TableCell>Compound</TableCell>
                      <TableCell>Element</TableCell>
                      <TableCell>Count</TableCell>
                      <TableCell>Oxidation Number</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {results.reactants.map((result, idx) => (
                      result.elements.map((elem, elemIdx) => (
                        <TableRow key={`reactant-${idx}-${elemIdx}`}>
                          {elemIdx === 0 && (
                            <TableCell rowSpan={result.elements.length}>
                              {result.compound}
                            </TableCell>
                          )}
                          <TableCell>{elem.element}</TableCell>
                          <TableCell>{elem.count}</TableCell>
                          <TableCell>{elem.oxidation}</TableCell>
                        </TableRow>
                      ))
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>

              <Typography variant="subtitle1" sx={{ mt: 3 }} gutterBottom>
                Products:
              </Typography>
              <TableContainer>
                <Table size="small">
                  <TableHead>
                    <TableRow>
                      <TableCell>Compound</TableCell>
                      <TableCell>Element</TableCell>
                      <TableCell>Count</TableCell>
                      <TableCell>Oxidation Number</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {results.products.map((result, idx) => (
                      result.elements.map((elem, elemIdx) => (
                        <TableRow key={`product-${idx}-${elemIdx}`}>
                          {elemIdx === 0 && (
                            <TableCell rowSpan={result.elements.length}>
                              {result.compound}
                            </TableCell>
                          )}
                          <TableCell>{elem.element}</TableCell>
                          <TableCell>{elem.count}</TableCell>
                          <TableCell>{elem.oxidation}</TableCell>
                        </TableRow>
                      ))
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            </Paper>
          )}
        </Box>
      </Container>
    </ThemeProvider>
  );
}

export default App; 