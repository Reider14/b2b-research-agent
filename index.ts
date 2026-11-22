import OpenAI from "openai";
import { z } from "zod";
import * as dotenv from "dotenv";

dotenv.config();


// 1. Definir schema de validacao com zod

const EmpresaSchema = z.object({
    nome: z.string(),
    setor: z.string(),
    tecnologias: z.array(z.string()),
    resumoModeloNegocio: z
        .string()
        .describe("Resuma o modelo de negocio em no maximo 2 frases"),
    estimativaFuncionarios: z
        .number()
        .nullable()
        .describe("Estimativa aproximada. Use null se nao souber."),
    nivelConfianca: z
        .enum(["alto", "medio", "baixo"])
        .describe("Nivel de certeza sobre os dados informados."),

});

type Empresa = z.infer<typeof EmpresaSchema>;

const { $schema: __, ...empresaJsonSchema } = z.toJSONSchema(EmpresaSchema);

async function pesquisarEmpresa(nomeEmpresa: string): Promise<Empresa>{
    const apiKey = process.env["OPENAI_API_KEY"];
    if (!apiKey) {
        throw new Error("OPENAI_API_KEY nao encontrada no .env");
    }

    // 2. Inicializar cliente OpenAI
    const genAI = new OpenAI(apiKey);
    //3. Chamar LLM com Structured Outputs

    const completation = await genAI.chat.completions.create({
        model: "gpt-4o-mini",
        temperature: 0,
        messages: [
            {
                role: "system",
                content: `Voce e um analista de pesquisa B2B rigoroso. Responda sempre em portugues. `
                    + `Nunca invente informacoes: se nao conhecer a empresa ou nao tiver certeza, `
                    + `defina nivelConfianca como 'baixo' e deixe claro no resumo que nao ha dados suficientes.`
            },
            {
                role: "user",
                content: `Analise a empresa "${nomeEmpresa}"`
            },
        ],
        response_format: {
            type: "json_schema",
            json_schema: {
                name: "empresa_b2b",
                strict: true,
                schema: empresaJsonSchema
            }
        }
        },
    );


    
    const textoBruto = completation.choices[0]?.message.content;
    if(!textoBruto){
        throw new Error("A OpenAI retornou uma resposta vazia.");
    }

    //4. Parsear o texto em objeto JS e validar contra o contrato Zod
    const jsonBruto: unknown = JSON.parse(textoBruto);
    const dadosValidados = EmpresaSchema.safeParse(jsonBruto);

    if (!dadosValidados.success) {
        throw new Error("Resposta do LLM nao seguiu o contrato EmpresaSchema.")
    }

    return dadosValidados.data;
}


async function main() {
    for(const empresa of ["Apple", "Kestrel Quantun Logistics", "SpaceX", "Starlink"]){
        console.log(`\nA pesquisar empresa ${empresa}...`);
        const resultado = await pesquisarEmpresa(empresa);
        console.log(resultado);
    }
    
}

main().catch((err) => {
    console.log("Erro na execucao:", err);
    process.exit(1);
})
